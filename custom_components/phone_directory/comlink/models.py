from dataclasses import dataclass


@dataclass
class Contact:
    """A single phone directory entry."""

    name: str
    number: str
