from .output_manager import OutputManager
from .outputs.grandstream import GrandstreamOutput


def publish_contacts(contacts):
    """Publish contacts to configured outputs."""

    manager = OutputManager()

    manager.add_output(GrandstreamOutput("/tmp/phonebook.xml"))

    manager.publish_all(contacts)
