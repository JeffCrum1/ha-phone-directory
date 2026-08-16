from ...output_models import OutputConfig, OutputDefinition, OutputField
from .grandstream import GrandstreamOutput


OUTPUT_DEFINITION = OutputDefinition(
    output_type="grandstream",
    label="Grandstream",
    fields=(
        OutputField(
            key="directory",
            label="Directory",
            type="string",
            required=True,
        ),
        OutputField(
            key="filename",
            label="Filename",
            type="string",
            required=False,
            default="phonebook.xml",
        ),
    ),
)

OUTPUT_CLASS = GrandstreamOutput


def create_output(config: OutputConfig) -> GrandstreamOutput:
    """Create a Grandstream output from configuration."""

    return OUTPUT_CLASS(
        config.data["directory"],
        config.data.get(
            "filename",
            "phonebook.xml",
        ),
    )


__all__ = [
    "GrandstreamOutput",
    "OUTPUT_CLASS",
    "OUTPUT_DEFINITION",
    "create_output",
]
