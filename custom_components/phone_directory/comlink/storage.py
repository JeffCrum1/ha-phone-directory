import json
from dataclasses import asdict
from pathlib import Path

from .models import Contact

DATA_FILE = Path(__file__).parent.parent / "contacts.json"


def load_contacts() -> list[Contact]:
    """Load all contacts from storage."""
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [Contact(**item) for item in data]


def save_contacts(contacts: list[Contact]) -> None:
    """Save all contacts to storage."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [asdict(contact) for contact in contacts],
            f,
            indent=2,
            ensure_ascii=False,
        )
