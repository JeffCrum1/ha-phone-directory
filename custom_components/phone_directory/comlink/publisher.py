"""Publish phone directory contacts to configured outputs."""

from .output_factory import create_output
from .output_manager import OutputManager
from .output_models import OutputConfig


def publish_contacts(
    outputs: list[OutputConfig],
    contacts,
) -> None:
    """Publish contacts to configured outputs."""

    manager = OutputManager()

    for output in outputs:
        manager.add_output(
            create_output(output),
        )

    manager.publish_all(contacts)
