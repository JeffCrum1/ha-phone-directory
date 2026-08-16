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
        data: dict,
    ) -> None:
        """Add an output."""

        outputs = [
            dict(output)
            for output in self._config_entry.data.get(
                "outputs",
                [],
            )
        ]

        output = {
            "output_id": str(uuid4()),
            "name": name,
            "output_type": output_type,
            **data,
        }

        outputs.append(output)

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
        data: dict,
    ) -> None:
        """Update an output."""

        outputs = []
        found = False

        for existing_output in self._config_entry.data.get(
            "outputs",
            [],
        ):
            output = dict(existing_output)

            if output["output_id"] == output_id:
                output["name"] = name
                output.update(data)
                found = True

            outputs.append(output)

        if not found:
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

    async def async_delete_output(
        self,
        output_id: str,
    ) -> None:
        """Delete an output."""

        existing_outputs = self._config_entry.data.get(
            "outputs",
            [],
        )

        outputs = [
            dict(output)
            for output in existing_outputs
            if output["output_id"] != output_id
        ]

        if len(outputs) == len(existing_outputs):
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
