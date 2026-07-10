"""Phone Directory integration."""

import logging

from homeassistant.core import HomeAssistant

LOGGER = logging.getLogger(__name__)

DOMAIN = "phone_directory"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Phone Directory integration."""

    LOGGER.info("Phone Directory setup complete")

    return True
