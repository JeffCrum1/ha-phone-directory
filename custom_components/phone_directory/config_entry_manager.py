"""Manage Home Assistant ConfigEntry data for Phone Directory."""

from homeassistant.config_entries import ConfigEntry

from .comlink.output_models import OutputConfig


class ConfigEntryManager:
    """Manage Phone Directory Home Assistant configuration."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the manager."""

        self._config_entry = config_entry

    def load_outputs(self) -> list[OutputConfig]:
        """Load configured outputs."""

        outputs = self._config_entry.data.get(
            "outputs",
            [],
        )

        return [OutputConfig.from_dict(output) for output in outputs]
