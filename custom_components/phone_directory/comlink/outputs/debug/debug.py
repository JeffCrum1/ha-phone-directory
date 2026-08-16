import logging


LOGGER = logging.getLogger(__name__)


class DebugOutput:
    """Debug output for testing the output pipeline."""

    def __init__(
        self,
        name: str,
        output_id: str,
    ):
        """Initialize the output."""

        self.name = name
        self.output_id = output_id

    def __str__(self) -> str:
        return f"Debug({self.name})"

    def publish(self, contacts) -> None:
        """Log contacts received by this output."""

        LOGGER.debug(
            "Phone Directory: Debug output '%s' (%s) " "received %d contacts: %s",
            self.name,
            self.output_id,
            len(contacts),
            contacts,
        )

        LOGGER.debug(
            "Phone Directory: Debug output '%s' published successfully",
            self.name,
        )
