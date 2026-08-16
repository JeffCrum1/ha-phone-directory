"""Manage Home Assistant ConfigEntry data for Phone Directory."""

from uuid import uuid4

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .comlink.output_models import OutputConfig


class ConfigEntryManager:
    """Manage Phone Directory Home Assistant configuration."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the manager."""

        self._hass = hass
        self._config_entry = config_entry

    def load_outputs(self) -> list[OutputConfig]:
        """Load configured outputs."""

        outputs = self._config_entry.data.get(
            "outputs",
            [],
        )

        return [OutputConfig.from_dict(output) for output in outputs]

    async def async_add_output(
        self,
        name: str,
        output_type: str,
    ) -> None:
        """Add an output."""

        outputs = [
            dict(output)
            for output in self._config_entry.data.get(
                "outputs",
                [],
            )
        ]

        outputs.append(
            {
                "output_id": str(uuid4()),
                "name": name,
                "output_type": output_type,
            }
        )

        self._hass.config_entries.async_update_entry(
            self._config_entry,
            data={
                **self._config_entry.data,
                "outputs": outputs,
            },
        )

    async def async_update_output(
        self,
        output_id: str,
        name: str,
    ) -> None:
        """Update an output."""

        outputs = []

        for existing_output in self._config_entry.data.get(
            "outputs",
            [],
        ):
            output = dict(existing_output)

            if output["output_id"] == output_id:
                output["name"] = name

            outputs.append(output)

        if not any(output["output_id"] == output_id for output in outputs):
            raise ValueError(
                f"Output not found: {output_id}",
            )

        self._hass.config_entries.async_update_entry(
            self._config_entry,
            data={
                **self._config_entry.data,
                "outputs": outputs,
            },
        )
