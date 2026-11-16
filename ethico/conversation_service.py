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