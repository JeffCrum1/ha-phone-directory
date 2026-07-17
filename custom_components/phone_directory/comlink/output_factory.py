from .output_models import OutputConfig
from .outputs.grandstream import GrandstreamOutput
from .outputs.debug import DebugOutput


def create_output(config: OutputConfig):
    """Create an output instance from configuration."""

    if config.output_type == "grandstream":
        return GrandstreamOutput(config.data["directory"])

    if config.output_type == "debug":
        return DebugOutput(config.data["name"])

    raise ValueError(f"Unknown output type: {config.output_type}")
