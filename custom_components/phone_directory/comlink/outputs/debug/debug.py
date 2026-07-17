import logging

LOGGER = logging.getLogger(__name__)


class DebugOutput:
    """Debug output for testing the output pipeline."""

    def __init__(self, name: str):
        self.name = name

    def publish(self, contacts) -> None:
        """Log contacts received by this output."""

        LOGGER.debug(
            "Debug output '%s' received %d contacts: %s",
            self.name,
            len(contacts),
            contacts,
        )
