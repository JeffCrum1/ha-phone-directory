from ...output_models import OutputConfig, OutputDefinition, OutputField
from .grandstream import GrandstreamOutput


OUTPUT_DEFINITION = OutputDefinition(
    output_type="grandstream",
    label="Grandstream",
    fields=(
        OutputField(
            key="userid",
            label="User ID",
            type="string",
            required=True,
        ),
        OutputField(
            key="password",
            label="Password",
            type="string",
            required=True,
            secret=True,
        ),
    ),
)

OUTPUT_CLASS = GrandstreamOutput


def create_output(config: OutputConfig) -> GrandstreamOutput:
    """Create a Grandstream output from configuration."""

    return OUTPUT_CLASS()


__all__ = [
    "GrandstreamOutput",
    "OUTPUT_CLASS",
    "OUTPUT_DEFINITION",
    "create_output",
]
