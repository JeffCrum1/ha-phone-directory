from .output_base import DirectoryOutput


class OutputManager:
    """Manage phone directory outputs."""

    def __init__(self):
        self.outputs: list[DirectoryOutput] = []

    def add_output(self, output: DirectoryOutput) -> None:
        """Add an output destination."""
        self.outputs.append(output)

    def publish_all(self, contacts) -> None:
        """Publish contacts to all outputs."""

        for output in self.outputs:
            output.publish(contacts)
