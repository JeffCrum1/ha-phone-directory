from .output_models import OutputConfig
from .outputs.grandstream import GrandstreamOutput


def create_output(config: OutputConfig):
    """Create an output instance from configuration."""

    if config.output_type == "grandstream":
        return GrandstreamOutput(config.data["path"])

    raise ValueError(f"Unknown output type: {config.output_type}")
