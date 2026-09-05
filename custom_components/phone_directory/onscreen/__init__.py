"""Phone Directory onscreen frontend."""

from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant

URL_BASE = "/phone_directory"
RESOURCE_URL = f"{URL_BASE}/phone-directory-card.js"


async def async_setup(hass: HomeAssistant) -> None:
    """Set up the Phone Directory onscreen frontend."""

    frontend_path = Path(__file__).parent

    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                URL_BASE,
                str(frontend_path),
                False,
            )
        ]
    )

    lovelace = hass.data.get("lovelace")

    if lovelace is None:
        return

    resources = lovelace.resources

    if not hasattr(resources, "async_create_item"):
        return

    await resources.async_load()

    for resource in resources.async_items():
        if resource["url"] == RESOURCE_URL:
            return

    await resources.async_create_item(
        {
            "res_type": "module",
            "url": RESOURCE_URL,
        }
    )


async def async_remove(hass: HomeAssistant) -> None:
    """Remove the Phone Directory onscreen frontend."""

    lovelace = hass.data.get("lovelace")

    if lovelace is None:
        return

    resources = lovelace.resources

    if not hasattr(resources, "async_delete_item"):
        return

    await resources.async_load()

    for resource in resources.async_items():
        if resource["url"] == RESOURCE_URL:
            await resources.async_delete_item(resource["id"])
            return
