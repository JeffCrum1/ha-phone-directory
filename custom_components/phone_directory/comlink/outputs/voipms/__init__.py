from ...output_models import OutputConfig, OutputDefinition, OutputField
from .voipms import VoipmsOutput


OUTPUT_DEFINITION = OutputDefinition(
    output_type="voipms",
    label="VoIP.ms",
    fields=(
        OutputField(
            key="api_username",
            label="API Username",
            type="string",
            required=True,
        ),
        OutputField(
            key="api_password",
            label="API Password",
            type="string",
            required=True,
            secret=True,
        ),
    ),
)

OUTPUT_CLASS = VoipmsOutput


def create_output(config: OutputConfig) -> VoipmsOutput:
    """Create a VoIP.ms output from configuration."""

    return OUTPUT_CLASS(
        config.data["api_username"],
        config.data["api_password"],
    )


__all__ = [
    "VoipmsOutput",
    "OUTPUT_CLASS",
    "OUTPUT_DEFINITION",
    "create_output",
]
