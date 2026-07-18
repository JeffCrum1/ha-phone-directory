import json
from dataclasses import asdict
from pathlib import Path

from .models import Contact

DATA_DIR = Path("/config/phone_directory_data")
DATA_FILE = DATA_DIR / "contacts.json"


def load_contacts() -> list[Contact]:
    """Load all contacts from storage."""
    if not DATA_FILE.exists():
        return []

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

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


def add_contact(name: str, number: str) -> None:
    """Add a new phone directory entry."""

    contacts = load_contacts()

    if any(contact.name == name for contact in contacts):
        raise ValueError(f"Contact already exists: {name}")

    if any(contact.number == number for contact in contacts):
        raise ValueError(f"Number already exists: {number}")

    contacts.append(Contact(name=name, number=number))

    save_contacts(contacts)


def delete_contact(name: str) -> None:
    """Delete a phone directory entry."""

    contacts = load_contacts()

    contacts = [contact for contact in contacts if contact.name != name]

    save_contacts(contacts)


def change_contact(
    old_name: str,
    new_name: str,
    new_number: str,
) -> None:
    """Change a phone directory entry."""

    contacts = load_contacts()

    for contact in contacts:
        if contact.name == old_name:
            if new_name != old_name and any(c.name == new_name for c in contacts):
                raise ValueError(f"Contact already exists: {new_name}")

            if new_number != contact.number and any(
                c.number == new_number for c in contacts
            ):
                raise ValueError(f"Number already exists: {new_number}")

            contact.name = new_name
            contact.number = new_number

            save_contacts(contacts)
            return

    raise ValueError(f"Contact not found: {old_name}")
