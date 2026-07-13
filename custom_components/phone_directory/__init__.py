"""Phone Directory integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import publish_everything

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Phone Directory from a config entry."""

    await hass.async_add_executor_job(
        publish_everything,
    )

    LOGGER.info("Phone Directory setup complete")

    return True
