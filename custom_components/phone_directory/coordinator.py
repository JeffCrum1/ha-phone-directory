"""Coordinate Phone Directory operations."""

from .comlink.publisher import publish_contacts
from .comlink.storage import (
    add_contact,
    change_contact,
    delete_contact,
    load_contacts,
)


def publish_everything() -> None:
    """Load contacts and publish them to all configured outputs."""

    contacts = load_contacts()
    publish_contacts(contacts)


def add_directory_contact(
    name: str,
    number: str,
) -> None:
    """Add a contact and publish updates."""

    add_contact(
        name,
        number,
    )

    publish_everything()


def delete_directory_contact(
    name: str,
) -> None:
    """Delete a contact and publish updates."""

    delete_contact(name)

    publish_everything()


def change_directory_contact(
    old_name: str,
    new_name: str,
    new_number: str,
) -> None:
    """Change a contact and publish updates."""

    change_contact(
        old_name,
        new_name,
        new_number,
    )

    publish_everything()
