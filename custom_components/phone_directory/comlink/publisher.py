from .output_manager import OutputManager
from .output_factory import create_output
from .output_storage import load_outputs


def publish_contacts(contacts):
    """Publish contacts to configured outputs."""

    manager = OutputManager()

    outputs = load_outputs()

    for output_config in outputs:
        manager.add_output(create_output(output_config))

    manager.publish_all(contacts)
