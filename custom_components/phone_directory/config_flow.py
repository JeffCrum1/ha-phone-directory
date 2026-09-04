from uuid import uuid4

from homeassistant import config_entries
import voluptuous as vol
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
)

from .comlink.output_factory import async_get_output_definitions
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
                data={
                    "outputs": [],
                },
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
        self._selected_output_type = None
        self._new_output_id = None

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
        """Select an existing output."""

        config_manager: ConfigEntryManager = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]

        outputs = config_manager.load_outputs()

        if not outputs:
            return await self.async_step_init()

        if self._selected_output_id is None:
            if user_input is not None:
                self._selected_output_id = user_input["output_id"]

                return await self.async_step_output_actions()

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
                                mode="dropdown",
                            )
                        ),
                    }
                ),
            )

        return await self.async_step_output_actions()

    async def async_step_output_actions(self, user_input=None):
        """Choose what to do with an existing output."""

        config_manager: ConfigEntryManager = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]

        outputs = config_manager.load_outputs()

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
            if user_input["action"] == "configure":
                return await self.async_step_configure_existing_output()

            if user_input["action"] == "delete":
                return await self.async_step_delete_output()

        return self.async_show_form(
            step_id="output_actions",
            data_schema=vol.Schema(
                {
                    vol.Required("action"): SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                SelectOptionDict(
                                    value="configure",
                                    label="Configure Output",
                                ),
                                SelectOptionDict(
                                    value="delete",
                                    label="Delete Output",
                                ),
                            ],
                            mode="list",
                        )
                    ),
                }
            ),
            description_placeholders={
                "output_name": output.data["name"],
            },
        )

    async def async_step_configure_existing_output(
        self,
        user_input=None,
    ):
        """Configure an existing output."""

        config_manager: ConfigEntryManager = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]

        outputs = config_manager.load_outputs()

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

        definitions = await async_get_output_definitions(
            self.hass,
        )

        definition = next(
            (
                definition
                for definition in definitions
                if definition.output_type == output.output_type
            ),
            None,
        )

        if definition is None:
            self._selected_output_id = None
            return await self.async_step_init()

        if user_input is not None:
            output_data = {
                key: value for key, value in user_input.items() if key != "name"
            }

            await config_manager.async_update_output(
                output.output_id,
                name=user_input["name"],
                data=output_data,
            )

            self._selected_output_id = None

            return await self.async_step_init()

        defaults = {}

        if definition.get_default is not None:
            defaults = definition.get_default(
                self.hass,
                output.output_id,
            )

        schema = {
            vol.Required(
                "name",
                default=output.data["name"],
            ): str,
        }

        for field in definition.fields:
            current_value = output.data.get(
                field.key,
                defaults.get(
                    field.key,
                    field.default,
                ),
            )

            field_schema = (
                vol.Required(
                    field.key,
                    default=current_value,
                )
                if field.required
                else vol.Optional(
                    field.key,
                    default=current_value,
                )
            )

            schema[field_schema] = str

        return self.async_show_form(
            step_id="configure_existing_output",
            data_schema=vol.Schema(schema),
            description_placeholders={
                "output_type": definition.label,
            },
        )

    async def async_step_delete_output(self, user_input=None):
        """Confirm deletion of an output."""

        config_manager: ConfigEntryManager = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]

        outputs = config_manager.load_outputs()

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
            await config_manager.async_delete_output(
                output.output_id,
            )

            self._selected_output_id = None

            return await self.async_step_init()

        return self.async_show_form(
            step_id="delete_output",
            data_schema=vol.Schema({}),
            description_placeholders={
                "output_name": output.data["name"],
            },
        )

    async def async_step_add_output(self, user_input=None):
        """Select an output type to add."""

        definitions = await async_get_output_definitions(
            self.hass,
        )

        if user_input is not None:
            self._selected_output_type = user_input["output_type"]

            return await self.async_step_configure_new_output()

        output_options = [
            SelectOptionDict(
                value=definition.output_type,
                label=definition.label,
            )
            for definition in definitions
        ]

        return self.async_show_form(
            step_id="add_output",
            data_schema=vol.Schema(
                {
                    vol.Required("output_type"): SelectSelector(
                        SelectSelectorConfig(
                            options=output_options,
                            mode="dropdown",
                        )
                    ),
                }
            ),
        )

    async def async_step_configure_new_output(
        self,
        user_input=None,
    ):
        """Configure a new output."""

        if self._selected_output_type is None:
            return await self.async_step_add_output()

        if self._new_output_id is None:
            self._new_output_id = str(uuid4())

        definitions = await async_get_output_definitions(
            self.hass,
        )

        definition = next(
            (
                definition
                for definition in definitions
                if definition.output_type == self._selected_output_type
            ),
            None,
        )

        if definition is None:
            self._selected_output_type = None
            self._new_output_id = None
            return await self.async_step_add_output()

        if user_input is not None:
            config_manager: ConfigEntryManager = self.hass.data[DOMAIN][
                self.config_entry.entry_id
            ]

            output_data = {
                key: value for key, value in user_input.items() if key != "name"
            }

            await config_manager.async_add_output(
                output_id=self._new_output_id,
                name=user_input["name"],
                output_type=definition.output_type,
                data=output_data,
            )

            self._selected_output_type = None
            self._new_output_id = None

            return await self.async_step_init()

        defaults = {}

        if definition.get_default is not None:
            defaults = definition.get_default(
                self.hass,
                self._new_output_id,
            )

        schema = {
            vol.Required(
                "name",
                default=definition.label,
            ): str,
        }

        for field in definition.fields:
            default = defaults.get(
                field.key,
                field.default,
            )

            field_schema = (
                vol.Required(
                    field.key,
                    default=default,
                )
                if field.required
                else vol.Optional(
                    field.key,
                    default=default,
                )
            )

            schema[field_schema] = str

        return self.async_show_form(
            step_id="configure_new_output",
            data_schema=vol.Schema(schema),
            description_placeholders={
                "output_type": definition.label,
            },
        )
