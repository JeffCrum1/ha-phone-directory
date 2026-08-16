from .output_models import OutputConfig
from .outputs.grandstream import GrandstreamOutput
from .outputs.debug import DebugOutput
from .outputs.voipms import VoipmsOutput


def get_output_types() -> list[str]:
    """Return the supported output types."""

    return [
        "grandstream",
        "voipms",
        "debug",
    ]


def create_output(config: OutputConfig):
    """Create an output instance from configuration."""

    if config.output_type == "grandstream":
        return GrandstreamOutput(config.data["directory"])

    if config.output_type == "voipms":
        return VoipmsOutput(
            config.data["api_username"],
            config.data["api_password"],
        )

    if config.output_type == "debug":
        return DebugOutput(config.data["name"])

    raise ValueError(f"Unknown output type: {config.output_type}")
