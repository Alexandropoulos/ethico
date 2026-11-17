from typing import Any
from supabase import Client


def _insert_id(client: Client, table: str, payload: dict[str, Any]) -> str:
    response = (
        client.table(table)
        .insert(payload)
        .select("id")
        .execute()
    )
    if not response.data:
        raise RuntimeError(f"Could not insert a row into {table}.")
    return str(response.data[0]["id"])


def create_conversation(client: Client, user_id: str, title: str) -> str:
    return _insert_id(client, "conversations", {
        "user_id": user_id,
        "title": title or "New conversation",
    })



def list_conversations(client: Client, user_id: str) -> list[dict[str, str]]:
    """Return the user's conversations, newest first."""
    response = (
        client.table("conversations")
        .select("id, title")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return [
        {"id": str(row["id"]), "title": row["title"]}
        for row in (response.data or [])
    ]


def list_messages(
    client: Client, user_id: str, conversation_id: str
) -> list[dict[str, str]]:
    """Fetch messages in chronological order after checking ownership."""
    conversation = (
        client.table("conversations")
        .select("id")
        .eq("id", conversation_id)
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    if not conversation.data:
        raise ValueError("Conversation not found.")

    response = (
        client.table("messages")
        .select("role, content")
        .eq("conversation_id", conversation_id)
        .order("created_at")
        .execute()
    )
    return response.data or []


def save_message(
    client: Client, conversation_id: str, role: str, content: str
) -> str:
    if role not in {"user", "assistant", "system"}:
        raise ValueError("Unsupported message role.")
    return _insert_id(client, "messages", {
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
    })


def _update_conversation(
    client: Client, conversation_id: str, payload: dict[str, Any]
) -> None:
    response = (
        client.table("conversations")
        .update(payload)
        .eq("id", conversation_id)
        .select("id")
        .execute()
    )
    if not response.data:
        raise RuntimeError("Could not update the conversation.")


def set_conversation_title(
    client: Client, user_id: str, conversation_id: str, title: str
) -> None:
    """Name a user's as-yet untitled conversation without overwriting a rename."""
    response = (
        client.table("conversations")
        .update({"title": title})
        .eq("id", conversation_id)
        .eq("user_id", user_id)
        .eq("title", "New conversation")
        .select("id")
        .execute()
    )
    if not response.data:
        raise RuntimeError("Could not update conversation title.")


def save_situation(
    client: Client, conversation_id: str, situation: dict[str, Any]
) -> None:
    """Save the latest formulation and clear any older evaluation."""
    _update_conversation(client, conversation_id, {
        "dilemma": situation,
        "evaluation": None,
    })


def save_evaluation(
    client: Client, conversation_id: str, evaluation: dict[str, Any]
) -> None:
    """Save the evaluation directly on its conversation."""
    _update_conversation(client, conversation_id, {
        "evaluation": evaluation,
    })