"""Coordinate Phone Directory operations."""

import logging

from .comlink.publisher import publish_contacts
from .comlink.storage import (
    add_contact,
    change_contact,
    delete_contact,
    load_contacts,
)

LOGGER = logging.getLogger(__name__)


def publish_everything(outputs) -> None:
    """Load contacts and publish them to configured outputs."""

    contacts = load_contacts()

    publish_contacts(
        outputs,
        contacts,
    )

    LOGGER.info(
        "Phone Directory: Published %s contacts",
        len(contacts),
    )


def add_directory_contact(
    name: str,
    number: str,
    outputs,
) -> None:
    """Add a contact and publish updates."""

    add_contact(
        name,
        number,
    )

    LOGGER.info(
        "Phone Directory: Added contact %s",
        name,
    )

    publish_everything(outputs)


def delete_directory_contact(
    name: str,
    outputs,
) -> None:
    """Delete a contact and publish updates."""

    delete_contact(name)

    LOGGER.info(
        "Phone Directory: Deleted contact %s",
        name,
    )

    publish_everything(outputs)


def change_directory_contact(
    old_name: str,
    new_name: str,
    new_number: str,
    outputs,
) -> None:
    """Change a contact and publish updates."""

    change_contact(
        old_name,
        new_name,
        new_number,
    )

    LOGGER.info(
        "Phone Directory: Changed contact %s to %s",
        old_name,
        new_name,
    )

    publish_everything(outputs)
