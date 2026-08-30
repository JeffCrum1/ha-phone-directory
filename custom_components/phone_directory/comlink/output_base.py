from typing import Protocol


class DirectoryOutput(Protocol):
    """Contract for phone directory outputs."""

    def publish(self, contacts) -> None:
        """Publish contacts to this output."""
        ...


class HTTPOutput(Protocol):
    """Contract for outputs that provide an HTTP endpoint."""

    @property
    def http_path(self) -> str:
        """Return the HTTP endpoint path for this output."""
        ...

    @property
    def http_content_type(self) -> str:
        """Return the HTTP response content type."""
        ...

    def render(self, contacts) -> str:
        """Render contacts as the HTTP response body."""
        ...
