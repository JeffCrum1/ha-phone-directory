"""Phone Directory integration."""

import logging
from pathlib import Path

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .comlink.http import HTTPManager
from .config_entry_manager import ConfigEntryManager
from .const import DOMAIN
from .coordinator import (
    add_directory_contact,
    change_directory_contact,
    delete_directory_contact,
    publish_directory,
)

DATA_DIR = Path("/config/phone_directory_data")

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Phone Directory from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    config_manager = ConfigEntryManager(
        hass,
        entry,
    )

    hass.data[DOMAIN][entry.entry_id] = config_manager

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    http_manager = HTTPManager(hass)

    for output in config_manager.load_outputs():
        await http_manager.async_register_output(output)

    async def async_publish_service(call: ServiceCall) -> None:
        """Publish the phone directory."""

        outputs = config_manager.load_outputs()

        try:
            await hass.async_add_executor_job(
                publish_directory,
                outputs,
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
                call.data["contact_id"],
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
                call.data["contact_id"],
                call.data["name"],
                call.data["number"],
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
        schema=vol.Schema(
            {
                vol.Required("name"): str,
                vol.Required("number"): str,
            }
        ),
    )

    hass.services.async_register(
        DOMAIN,
        "delete_contact",
        async_delete_contact_service,
        schema=vol.Schema(
            {
                vol.Required("contact_id"): str,
            }
        ),
    )

    hass.services.async_register(
        DOMAIN,
        "change_contact",
        async_change_contact_service,
        schema=vol.Schema(
            {
                vol.Required("contact_id"): str,
                vol.Required("name"): str,
                vol.Required("number"): str,
            }
        ),
    )

    LOGGER.info("Phone Directory setup complete")

    return True
