from typing import Protocol


class DirectoryOutput(Protocol):
    """Contract for phone directory outputs."""

    def publish(self, contacts) -> None:
        """Publish contacts to this output."""
        ...
