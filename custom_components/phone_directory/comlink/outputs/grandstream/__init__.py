from homeassistant.helpers import network

from ...output_models import OutputConfig, OutputDefinition, OutputField
from .grandstream import GrandstreamOutput


def get_default(hass) -> dict:
    """Return default Grandstream configuration."""

    return {
        "base_url": network.get_url(hass),
    }


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
        OutputField(
            key="base_url",
            label="Base URL",
            type="string",
            required=True,
        ),
    ),
    get_default=get_default,
)

OUTPUT_CLASS = GrandstreamOutput


def create_output(config: OutputConfig) -> GrandstreamOutput:
    """Create a Grandstream output from configuration."""

    return OUTPUT_CLASS(config)


__all__ = [
    "GrandstreamOutput",
    "OUTPUT_CLASS",
    "OUTPUT_DEFINITION",
    "create_output",
]
