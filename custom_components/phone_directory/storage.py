import json
from dataclasses import asdict
from pathlib import Path
from uuid import uuid4

from .models import Contact

DATA_DIR = Path("/config/phone_directory_data")
DATA_FILE = DATA_DIR / "contacts.json"


def load_contacts() -> list[Contact]:
    """Load all contacts from storage."""

    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        items = data.get("contacts", [])
    else:
        # Support the previous list-based storage format.
        items = data

    contacts = []

    for item in items:
        contacts.append(
            Contact(
                name=item["name"],
                number=item["number"],
                contact_id=item.get(
                    "contact_id",
                    str(uuid4()),
                ),
            )
        )

    return contacts


def save_contacts(contacts: list[Contact]) -> None:
    """Save all contacts to storage."""

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "contacts": [asdict(contact) for contact in contacts],
            },
            f,
            indent=2,
            ensure_ascii=False,
        )


def get_contact(contact_id: str) -> Contact:
    """Get a contact by ID."""

    contacts = load_contacts()

    for contact in contacts:
        if contact.contact_id == contact_id:
            return contact

    raise ValueError(
        f"Contact not found: {contact_id}",
    )


def add_contact(name: str, number: str) -> Contact:
    """Add a new phone directory entry."""

    contacts = load_contacts()

    if any(contact.name == name for contact in contacts):
        raise ValueError(
            f"Contact already exists: {name}",
        )

    if any(contact.number == number for contact in contacts):
        raise ValueError(
            f"Number already exists: {number}",
        )

    contact = Contact(
        name=name,
        number=number,
    )

    contacts.append(contact)

    save_contacts(contacts)

    return contact


def delete_contact(contact_id: str) -> None:
    """Delete a phone directory entry."""

    contacts = load_contacts()

    updated_contacts = [
        contact for contact in contacts if contact.contact_id != contact_id
    ]

    if len(updated_contacts) == len(contacts):
        raise ValueError(
            f"Contact not found: {contact_id}",
        )

    save_contacts(updated_contacts)


def change_contact(
    contact_id: str,
    new_name: str,
    new_number: str,
) -> Contact:
    """Change a phone directory entry."""

    contacts = load_contacts()

    contact = next(
        (contact for contact in contacts if contact.contact_id == contact_id),
        None,
    )

    if contact is None:
        raise ValueError(
            f"Contact not found: {contact_id}",
        )

    if new_name != contact.name and any(other.name == new_name for other in contacts):
        raise ValueError(
            f"Contact already exists: {new_name}",
        )

    if new_number != contact.number and any(
        other.number == new_number for other in contacts
    ):
        raise ValueError(
            f"Number already exists: {new_number}",
        )

    contact.name = new_name
    contact.number = new_number

    save_contacts(contacts)

    return contact
