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
        """Publish contacts to all outputs that support publishing."""

        for output in self.outputs:
            LOGGER.debug(
                "Phone Directory: output diagnostic: type=%s, repr=%r, has_publish=%s",
                type(output),
                output,
                hasattr(output, "publish"),
            )

            publish = getattr(output, "publish", None)

            if publish is None:
                LOGGER.debug(
                    "Phone Directory: output %s does not support publishing",
                    output,
                )
                continue

            try:
                LOGGER.info(
                    "Phone Directory: publishing to %s",
                    output,
                )

                publish(contacts)

                LOGGER.info(
                    "Phone Directory: published successfully to %s (%s contacts)",
                    output,
                    len(contacts),
                )

            except Exception as err:
                LOGGER.error(
                    "Phone Directory: publish failed for %s: %s",
                    output,
                    err,
exc_info=True,
                )
