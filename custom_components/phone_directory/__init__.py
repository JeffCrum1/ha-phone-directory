"""Phone Directory integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN
from .coordinator import (
    add_directory_contact,
    change_directory_contact,
    delete_directory_contact,
    publish_everything,
)

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Phone Directory from a config entry."""

    async def async_publish_service(call: ServiceCall) -> None:
        """Publish the phone directory."""

        try:
            await hass.async_add_executor_job(
                publish_everything,
            )
        except Exception:
            LOGGER.exception(
                "Phone Directory: unexpected publish failure",
            )

    async def async_add_contact_service(call: ServiceCall) -> None:
        """Add a phone directory contact."""

        try:
            await hass.async_add_executor_job(
                add_directory_contact,
                call.data["name"],
                call.data["number"],
            )
        except ValueError as err:
            LOGGER.error(
                "Phone Directory: %s",
                err,
            )

    async def async_delete_contact_service(call: ServiceCall) -> None:
        """Delete a phone directory contact."""

        try:
            await hass.async_add_executor_job(
                delete_directory_contact,
                call.data["name"],
            )
        except ValueError as err:
            LOGGER.error(
                "Phone Directory: %s",
                err,
            )

    async def async_change_contact_service(call: ServiceCall) -> None:
        """Change a phone directory contact."""

        try:
            await hass.async_add_executor_job(
                change_directory_contact,
                call.data["old_name"],
                call.data["new_name"],
                call.data["new_number"],
            )
        except ValueError as err:
            LOGGER.error(
                "Phone Directory: %s",
                err,
            )

    hass.services.async_register(
        DOMAIN,
        "publish",
        async_publish_service,
    )

    hass.services.async_register(
        DOMAIN,
        "add_contact",
        async_add_contact_service,
    )

    hass.services.async_register(
        DOMAIN,
        "delete_contact",
        async_delete_contact_service,
    )

    hass.services.async_register(
        DOMAIN,
        "change_contact",
        async_change_contact_service,
    )

    LOGGER.info("Phone Directory setup complete")

    return True
