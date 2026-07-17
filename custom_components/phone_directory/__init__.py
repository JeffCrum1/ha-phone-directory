"""Phone Directory integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN
from .coordinator import publish_everything

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Phone Directory from a config entry."""

    async def async_publish_service(call: ServiceCall) -> None:
        """Publish the phone directory."""

        await hass.async_add_executor_job(
            publish_everything,
        )

    hass.services.async_register(
        DOMAIN,
        "publish",
        async_publish_service,
    )

    await hass.async_add_executor_job(
        publish_everything,
    )

    LOGGER.info("Phone Directory setup complete")

    return True
