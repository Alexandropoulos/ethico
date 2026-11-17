import asyncio
import json
import logging
import os
import tempfile
from pathlib import Path

import reflex as rx
from dotenv import load_dotenv
from openai import APIError, AsyncOpenAI

from ethico.auth_state import AuthState
from ethico.constants import (
    EXPLAIN_PROMPT, 
    OPENAI_TOOLS, 
    SYSTEM_PROMPT,
    TITLE_GENERATION_PROMPT,
    TROLLEY_TEST_PROMPT
)
from ethico.conversation_service import (
    create_conversation,
    list_conversations,
    list_messages,
    save_evaluation,
    save_message,
    save_situation,
    set_conversation_title,
)
from ethico.evaluator import evaluate_dilemma
from ethico.validator import UnifiedModel


MODEL = "gpt-4o-mini"
logger = logging.getLogger(__name__)
load_dotenv()


class State(rx.State):
    question: str = ""
    chat_history: list[tuple[str, str]] = []
    processing: bool = False
    error: str = ""
    dilemma_json: str = ""
    dilemma_panel_open: bool = False
    
    conversation_id: str = ""
    conversations: list[dict[str, str]] = []

    # Incremented whenever chats or users change so an old stream cannot
    # write into a different conversation.
    chat_generation: int = 0

    @rx.event
    def set_question(self, value: str):
        self.question = value

    @rx.event
    def toggle_dilemma_panel(self):
        self.dilemma_panel_open = not self.dilemma_panel_open

    def _clear_chat(self):
        """Called by AuthState on login and logout."""
        self.question = ""
        self.chat_history = []
        self.dilemma_json = ""
        self.dilemma_panel_open = False
        self.processing = False
        self.error = ""
        self.conversation_id = ""
        self.conversations = []
        self.chat_generation += 1

    @rx.event
    async def load_conversations(self):
        """Refresh the sidebar from the current user's conversations."""
        auth = await self.get_state(AuthState)
        try:
            client = auth._authenticated_client()
            user_id = auth.user_id
            generation = self.chat_generation
            rows = await asyncio.to_thread(list_conversations, client, user_id)
            if self.chat_generation == generation:
                self.conversations = rows
        except Exception:
            logger.exception("Could not load conversations")
            self.error = "Could not load your conversations."

    @rx.event
    async def open_conversation(self, conversation_id: str):
        """Switch chat context to the selected conversation."""
        if self.processing:
            return
        if self.conversation_id == conversation_id:
            return rx.redirect("/")

        auth = await self.get_state(AuthState)
        try:
            client = auth._authenticated_client()
            user_id = auth.user_id
            generation = self.chat_generation
            rows = await asyncio.to_thread(
                list_messages, client, user_id, conversation_id
            )
            # The saved dilemma belongs to the conversation, not its messages.
            record = await asyncio.to_thread(
                lambda: client.table("conversations")
                .select("dilemma,evaluation")
                .eq("id", conversation_id)
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            if self.chat_generation != generation:
                return
        except Exception:
            logger.exception("Could not open conversation")
            self.error = "Could not open this conversation."
            return

        history: list[tuple[str, str]] = []
        for message in rows:
            role, content = message["role"], message["content"]
            if role == "user":
                history.append((content, ""))
            elif role == "assistant" and history:
                question, answer = history[-1]
                history[-1] = (question, answer + content)

        self.chat_history = history
        saved = record.data or {}
        dilemma = saved.get("dilemma") if saved.get("evaluation") is not None else None
        self.dilemma_json = json.dumps(dilemma, indent=2, ensure_ascii=False) if dilemma is not None else ""
        self.dilemma_panel_open = bool(self.dilemma_json)
        self.conversation_id = conversation_id
        self.question = ""
        self.error = ""
        self.chat_generation += 1
        return rx.redirect("/")

    @rx.event
    def new_conversation(self):
        """Start a fresh chat without removing the sidebar history."""
        if self.processing:
            return
        self.conversation_id = ""
        self.chat_history = []
        self.dilemma_json = ""
        self.dilemma_panel_open = False
        self.question = ""
        self.error = ""
        self.chat_generation += 1
        return rx.redirect("/")

    @rx.event(background=True)
    async def answer(self):
        async with self:
            question = self.question.strip()
            if not question or self.processing:
                return

            auth = await self.get_state(AuthState)
            try:
                supabase = auth._authenticated_client()
                user_id = auth.user_id  
            except Exception:
                logger.warning("Rejected unauthenticated chat event", exc_info=True)
                self.error = "Please log in before using the chat."
                return

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                self.error = "Set OPENAI_API_KEY and restart the app."
                return

            self.processing = True
            self.error = ""
            self.question = ""
            self.chat_history.append((question, ""))
            messages = self._create_message_list()
            conversation_id = self.conversation_id
            generation = self.chat_generation
        yield

        user_saved = False
        assistant_saved = False
        answer_parts: list[str] = []

        try:
            if not conversation_id:
                conversation_id = await asyncio.to_thread(
                    create_conversation, supabase, user_id, "New conversation"
                )
                async with self:
                    if self.chat_generation != generation:
                        return
                    self.conversation_id = conversation_id
                    self.conversations.insert(0, {
                        "id": conversation_id,
                        "title": "New conversation",
                    })
                yield

            async with self:
                if self.chat_generation != generation:
                    return

            
            await asyncio.to_thread(
                save_message, supabase, conversation_id, "user", question
            )
            user_saved = True

            async with AsyncOpenAI(api_key=api_key) as openai:
                if question.lower() == "evaluate":
                    situation_path = await self._extract_dilemma(openai, messages)
                    evaluation_path = Path(situation_path).parent / "evaluation.json"

                    with open(situation_path, encoding="utf-8") as f:
                        situation = json.load(f)

                    await asyncio.to_thread(
                        save_situation, supabase, conversation_id, situation
                    )

                    await asyncio.to_thread(
                        evaluate_dilemma,
                        situation_path,
                        str(evaluation_path),
                    )
                    with open(evaluation_path, encoding="utf-8") as f:
                        evaluation = json.load(f)
                    
                    await asyncio.to_thread(
                        save_evaluation, supabase, conversation_id, evaluation
                    )

                    async with self:
                        if self.chat_generation != generation:
                            return
                        self.dilemma_json = Path(situation_path).read_text(encoding="utf-8")
                        self.dilemma_panel_open = True
                    messages.append({
                        "role": "system",
                        "content": EXPLAIN_PROMPT.format(
                            evaluation=json.dumps(evaluation, indent=2)
                        ),
                    })

                stream = await openai.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    stream=True,
                )
                async with stream:
                    async for chunk in stream:
                        if not chunk.choices:
                            continue
                        delta = chunk.choices[0].delta.content
                        if not delta:
                            continue

                        async with self:
                            if self.chat_generation != generation:
                                # User logged out or started a new chat.
                                return
                            previous = self.chat_history[-1][1]
                            self.chat_history[-1] = (question, previous + delta)
                        answer_parts.append(delta)
                        yield

            async with self:
                if self.chat_generation != generation:
                    return

            if answer_parts:
                await asyncio.to_thread(
                    save_message,
                    supabase,
                    conversation_id,
                    "assistant",
                    "".join(answer_parts),
                )
                assistant_saved = True

                # Title only conversations that have not yet been named.
                # A generic opener should not become a misleading title.
                async with self:
                    needs_title = (
                        self.chat_generation == generation
                        and any(
                            c["id"] == conversation_id
                            and c["title"] == "New conversation"
                            for c in self.conversations
                        )
                    )

                if needs_title and question.lower().strip(" !?.") not in {
                    "hi", "hello", "hey", "thanks", "thank you", "γεια", "γειά",
                }:
                    try:
                        title_messages = [
                            *messages,
                            {"role": "assistant", "content": "".join(answer_parts)},
                        ]
                        async with AsyncOpenAI(
                            api_key=api_key, timeout=8.0, max_retries=0
                        ) as title_client:
                            title = await self._generate_conversation_title(
                                title_client, title_messages
                            )
                        if title:
                            await asyncio.to_thread(
                                set_conversation_title,
                                supabase, user_id, conversation_id, title,
                            )
                            async with self:
                                if self.chat_generation == generation:
                                    self.conversations = [
                                        {**c, "title": title}
                                        if c["id"] == conversation_id
                                        and c["title"] == "New conversation"
                                        else c
                                        for c in self.conversations
                                    ]
                            yield
                    except Exception:
                        # Naming is optional; it must never fail the chat reply.
                        logger.exception("Could not generate or save conversation title")

        except APIError:
            logger.exception("OpenAI request failed")
            async with self:
                if self.chat_generation == generation:
                    self.error = "The request failed. Check your API access and try again."
        except Exception:
            logger.exception("Chat processing or persistence failed")
            async with self:
                if self.chat_generation == generation:
                    self.error = "Could not process or save this message. Check the server logs."
                    if not user_saved:
                        self.chat_history.pop()
                        self.question = question
        finally:
            if user_saved and answer_parts and not assistant_saved:
                async with self:
                    same_chat = self.chat_generation == generation
                if same_chat:
                    try:
                        await asyncio.to_thread(
                            save_message,
                            supabase,
                            conversation_id,
                            "assistant",
                            "".join(answer_parts),
                        )
                    except Exception:
                        logger.exception("Could not save partial assistant reply")

            async with self:
                if self.chat_generation == generation:
                    self.processing = False
            yield

    async def _generate_conversation_title(
        self, client: AsyncOpenAI, messages: list[dict[str, str]]
    ) -> str:
        """Summarize the first meaningful exchange into a sidebar title."""
        transcript = "\n".join(
            f"{m['role']}: {m['content'][:500]}"
            for m in messages if m["role"] in {"user", "assistant"}
        )[-2500:]
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (TITLE_GENERATION_PROMPT),
                },
                {"role": "user", "content": transcript},
            ],
            temperature=0.2,
            max_completion_tokens=32,
        )
        title = (response.choices[0].message.content or "").split("\n", 1)[0]
        title = title.strip().strip('"\'`').strip()
        if not title or title.upper() == "NONE":
            return ""
        if len(title) > 60:
            title = title[:60].rsplit(" ", 1)[0] or title[:60]
        return title

    def _create_message_list(self) -> list[dict[str, str]]:
        messages = [{"role": "system", "content": TROLLEY_TEST_PROMPT}]
        for previous_question, previous_answer in self.chat_history:
            messages.append({"role": "user", "content": previous_question})
            if previous_answer:
                messages.append({"role": "assistant", "content": previous_answer})
        return messages

    async def _extract_dilemma(
        self, client: AsyncOpenAI, messages: list[dict]
    ) -> str:
        tool = next(
            t for t in OPENAI_TOOLS
            if t["function"]["name"] == "extract_dilemma"
        )

        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=[tool],
            tool_choice={
                "type": "function",
                "function": {"name": "extract_dilemma"},
            },
        )
        
        tool_calls = response.choices[0].message.tool_calls
        if not tool_calls:
            raise ValueError("Failed to extract dilemma.")

        extracted_model = json.loads(tool_calls[0].function.arguments)
        UnifiedModel.model_validate(extracted_model)

        situation_path = Path(tempfile.mkdtemp(prefix="thufir_")) / "situation.json"
        with open(situation_path, "w", encoding="utf-8") as f:
            json.dump(extracted_model, f, indent=2)
        return str(situation_path)
