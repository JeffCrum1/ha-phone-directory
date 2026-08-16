from homeassistant import config_entries
import voluptuous as vol
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
)

from .config_entry_manager import ConfigEntryManager
from .const import DOMAIN


class PhoneDirectoryConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow for Phone Directory."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup."""

        if user_input is not None:
            return self.async_create_entry(
                title="Phone Directory",
                data={},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow."""

        return PhoneDirectoryOptionsFlowHandler()


class PhoneDirectoryOptionsFlowHandler(
    config_entries.OptionsFlow,
):
    """Handle Phone Directory options."""

    def __init__(self) -> None:
        """Initialize options flow."""

        self._selected_output_id = None

    async def async_step_init(self, user_input=None):
        """Manage Phone Directory options."""

        config_manager: ConfigEntryManager = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]

        outputs = config_manager.load_outputs()

        menu_options = {
            "configure_output": "Configure Output",
            "add_output": "Add Output",
        }

        if not outputs:
            menu_options.pop("configure_output")

        return self.async_show_menu(
            step_id="init",
            menu_options=menu_options,
        )

    async def async_step_configure_output(
        self,
        user_input=None,
    ):
        """Select or configure an output."""

        config_manager: ConfigEntryManager = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]

        outputs = config_manager.load_outputs()

        if not outputs:
            return await self.async_step_init()

        if self._selected_output_id is not None:
            output = next(
                (
                    output
                    for output in outputs
                    if output.output_id == self._selected_output_id
                ),
                None,
            )

            if output is None:
                self._selected_output_id = None
                return await self.async_step_init()

            if user_input is not None:
                await config_manager.async_update_output(
                    output.output_id,
                    name=user_input["name"],
                )

                self._selected_output_id = None

                return await self.async_step_init()

            return self.async_show_form(
                step_id="configure_output",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            "name",
                            default=output.data["name"],
                        ): str,
                    }
                ),
                description_placeholders={
                    "output_type": output.output_type,
                },
            )

        if user_input is not None:
            self._selected_output_id = user_input["output_id"]

            return await self.async_step_configure_output()

        options = [
            SelectOptionDict(
                value=output.output_id,
                label=output.data["name"],
            )
            for output in outputs
        ]

        return self.async_show_form(
            step_id="configure_output",
            data_schema=vol.Schema(
                {
                    vol.Required("output_id"): SelectSelector(
                        SelectSelectorConfig(
                            options=options,
                        )
                    ),
                }
            ),
        )

    async def async_step_add_output(self, user_input=None):
        """Add an output."""

        if user_input is not None:
            config_manager: ConfigEntryManager = self.hass.data[DOMAIN][
                self.config_entry.entry_id
            ]

            await config_manager.async_add_output(
                name=user_input["name"],
                output_type="grandstream",
            )

            return await self.async_step_init()

        return self.async_show_form(
            step_id="add_output",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "name",
                        default="House Phones",
                    ): str,
                }
            ),
        )
