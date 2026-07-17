import logging

LOGGER = logging.getLogger(__name__)


class OutputManager:
    """Manage phone directory outputs."""

    def __init__(self):
        self.outputs = []

    def add_output(self, output) -> None:
        """Add an output."""

        self.outputs.append(output)

    def publish_all(self, contacts) -> None:
        """Publish contacts to all outputs."""

        for output in self.outputs:
            try:
                LOGGER.info(
                    "Phone Directory: publishing to %s",
                    output,
                )

                output.publish(contacts)

                LOGGER.info(
                    "Phone Directory: published successfully to %s (%s contacts)",
                    output,
                    len(contacts),
                )

            except Exception:
                LOGGER.exception(
                    "Phone Directory: publish failed for %s",
                    output,
                )
