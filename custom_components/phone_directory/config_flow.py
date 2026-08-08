class PhoneDirectoryOptionsFlowHandler(
    config_entries.OptionsFlow,
):
    """Handle Phone Directory options."""

    def __init__(self, config_entry):
        """Initialize options flow."""

        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage Phone Directory options."""

        return self.async_show_menu(
            step_id="init",
            menu_options={
                "add_output": "Add Output",
            },
        )

    async def async_step_add_output(self, user_input=None):
        """Add an output."""

        return self.async_show_form(
            step_id="add_output",
            data_schema=vol.Schema({}),
        )
