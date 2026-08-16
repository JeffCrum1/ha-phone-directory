"""Coordinate Phone Directory operations."""

import logging

from .models import Contact
from .storage import (
    add_contact,
    change_contact,
    delete_contact,
    get_contact,
    load_contacts,
)

LOGGER = logging.getLogger(__name__)


def get_directory_contacts() -> list[Contact]:
    """Return all phone directory contacts."""

    return load_contacts()


def get_directory_contact(
    contact_id: str,
) -> Contact:
    """Return a phone directory contact by ID."""

    return get_contact(contact_id)


def add_directory_contact(
    name: str,
    number: str,
) -> Contact:
    """Add a contact."""

    contact = add_contact(
        name,
        number,
    )

    LOGGER.info(
        "Phone Directory: Added contact %s",
        name,
    )

    return contact


def delete_directory_contact(
    contact_id: str,
) -> None:
    """Delete a contact."""

    delete_contact(
        contact_id,
    )

    LOGGER.info(
        "Phone Directory: Deleted contact %s",
        contact_id,
    )


def change_directory_contact(
    contact_id: str,
    new_name: str,
    new_number: str,
) -> Contact:
    """Change a contact."""

    contact = change_contact(
        contact_id,
        new_name,
        new_number,
    )

    LOGGER.info(
        "Phone Directory: Changed contact %s",
        contact_id,
    )

    return contact
