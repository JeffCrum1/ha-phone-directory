from .outputs.grandstream import GrandstreamOutput


class OutputManager:
    """Manage phone directory outputs."""

    def __init__(self):
        self.outputs = []

    def add_output(self, output):
        """Add an output destination."""
        self.outputs.append(output)

    def publish_all(self, contacts):
        """Publish contacts to all outputs."""
        for output in self.outputs:
            output.publish(contacts)
