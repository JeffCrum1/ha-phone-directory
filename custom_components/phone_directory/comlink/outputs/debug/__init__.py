from ...output_models import OutputConfig, OutputDefinition
from .debug import DebugOutput


OUTPUT_DEFINITION = OutputDefinition(
    output_type="debug",
    label="Debug",
    fields=(),
)

OUTPUT_CLASS = DebugOutput


def create_output(config: OutputConfig) -> DebugOutput:
    """Create a Debug output from configuration."""

    return OUTPUT_CLASS(
        config.data["name"],
        config.data["output_id"],
    )


__all__ = [
    "DebugOutput",
    "OUTPUT_CLASS",
    "OUTPUT_DEFINITION",
    "create_output",
]
