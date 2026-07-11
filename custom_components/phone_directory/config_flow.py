"""Config flow for Phone Directory."""

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN


class PhoneDirectoryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
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
            data_schema=None,
        )
