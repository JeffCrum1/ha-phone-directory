"""Coordinate Phone Directory publishing."""

from .comlink.publisher import publish_contacts
from .comlink.storage import load_contacts


def publish_everything() -> None:
    """Load contacts and publish them to all configured outputs."""

    contacts = load_contacts()
    publish_contacts(contacts)
