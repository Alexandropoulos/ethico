
import json
import os
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID

from dotenv import load_dotenv
from faker import Faker
from supabase import create_client


# --------------------------------------------------
# Configuration
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
TEST_CASES_DIR = ROOT / "data" / "test_cases"

load_dotenv(ROOT / ".env")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

USER_IDS = [
    user_id.strip()
    for user_id in os.environ["SUPABASE_TEST_USER_IDS"].split(",")
    if user_id.strip()
]

CONVERSATION_COUNT = 18
SEED = 42

rng = random.Random(SEED)
fake = Faker()
fake.seed_instance(SEED)


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_test_cases():
    """Load distinct, successfully evaluated test cases."""

    if not TEST_CASES_DIR.is_dir():
        raise FileNotFoundError(
            f"Directory not found: {TEST_CASES_DIR}"
        )

    cases = []

    for directory in sorted(TEST_CASES_DIR.iterdir()):
        if not directory.is_dir():
            continue

        situation_path = directory / "situation.json"
        evaluation_path = directory / "evaluation.json"

        # Only use complete test cases.
        if not (
            situation_path.is_file()
            and evaluation_path.is_file()
        ):
            continue

        situation = load_json(situation_path)
        evaluation = load_json(evaluation_path)

        cases.append({
            "name": directory.name,
            "situation": situation,
            "evaluation": evaluation,
        })

    if len(cases) < CONVERSATION_COUNT:
        raise ValueError(
            f"Need {CONVERSATION_COUNT} complete test cases, "
            f"but found only {len(cases)}."
        )

    return rng.sample(cases, CONVERSATION_COUNT)


def generate_messages(conversation_id, created_at, count):
    """Generate chronologically ordered Faker messages."""

    messages = []

    for index in range(count):
        role = "user" if index % 2 == 0 else "assistant"

        # Faker generates fictional placeholder content.
        content = fake.paragraph(
            nb_sentences=rng.randint(2, 5)
        )

        timestamp = created_at + timedelta(
            minutes=(index + 1) * rng.randint(1, 3)
        )

        messages.append({
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "created_at": timestamp.isoformat(),
        })

    return messages


# --------------------------------------------------
# Seeding
# --------------------------------------------------

def seed_database():
    if len(USER_IDS) != 3:
        raise ValueError(
            "Exactly 3 user UUIDs are required in "
            "SUPABASE_TEST_USER_IDS."
        )

    for user_id in USER_IDS:
        UUID(user_id)

    if len(set(USER_IDS)) != 3:
        raise ValueError("Test user UUIDs must be distinct.")

    cases = get_test_cases()

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY,
    )

    base_time = datetime.now(timezone.utc) - timedelta(
        days=30
    )

    total_messages = 0

    for index, case in enumerate(cases):
        user_id = USER_IDS[index % 3]

        created_at = base_time + timedelta(
            days=index,
            hours=rng.randint(0, 12),
        )

        # 10 conversations with 8 messages each.
        # 10 conversations with 10 messages each.
        # Total: 180 messages.
        message_count = 8 if index < 10 else 10

        conversation = {
            "user_id": user_id,
            "title": case["name"].replace("_", " ").title(),
            "dilemma": case["situation"],
            "evaluation": case["evaluation"],
            "created_at": created_at.isoformat(),
        }

        result = (
            supabase.table("conversations")
            .insert(conversation)
            .execute()
        )

        conversation_id = result.data[0]["id"]

        messages = generate_messages(
            conversation_id,
            created_at,
            message_count,
        )

        (
            supabase.table("messages")
            .insert(messages)
            .execute()
        )

        total_messages += len(messages)

        print(
            f"[{index + 1:02}/{CONVERSATION_COUNT}] "
            f"{conversation['title']} "
            f"({message_count} messages)"
        )

    print("\nSeeding complete.")
    print(f"Conversations: {len(cases)}")
    print(f"Messages: {total_messages}")
    print(f"Users: {len(USER_IDS)}")


if __name__ == "__main__":
    seed_database()
