"""Phone Directory integration."""

import logging
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .config_entry_manager import ConfigEntryManager
from .const import DOMAIN
from .coordinator import (
    add_directory_contact,
    change_directory_contact,
    delete_directory_contact,
    publish_everything,
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

    outputs = config_manager.load_outputs()

    async def async_publish_service(call: ServiceCall) -> None:
        """Publish the phone directory."""

        try:
            await hass.async_add_executor_job(
                publish_everything,
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
                outputs,
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
                outputs,
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
                outputs,
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
