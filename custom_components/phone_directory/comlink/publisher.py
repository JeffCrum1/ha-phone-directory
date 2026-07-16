from .output_manager import OutputManager
from .output_factory import create_output
from .output_models import OutputConfig


def publish_contacts(contacts):
    """Publish contacts to configured outputs."""

    manager = OutputManager()

    outputs = [
        OutputConfig(
            output_id="grandstream-home",
            output_type="grandstream",
            data={
                "directory": "/tmp/grandstream/home",
            },
        ),
    ]

    for output_config in outputs:
        manager.add_output(create_output(output_config))

    manager.publish_all(contacts)
