from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Contact:
    """A single phone directory entry."""

    name: str
    number: str
    contact_id: str = field(
        default_factory=lambda: str(uuid4()),
    )
