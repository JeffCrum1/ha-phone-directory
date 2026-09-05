"""Phone Directory WebSocket API."""

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant

from .coordinator import get_directory_contacts


@websocket_api.websocket_command(
    {
        vol.Required("type"): "phone_directory/get_contacts",
    }
)
@websocket_api.async_response
async def websocket_get_contacts(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict,
) -> None:
    """Return all phone directory contacts."""

    contacts = await hass.async_add_executor_job(
        get_directory_contacts,
    )

    connection.send_result(
        msg["id"],
        {
            "contacts": [
                {
                    "contact_id": contact.contact_id,
                    "name": contact.name,
                    "number": contact.number,
                }
                for contact in contacts
            ]
        },
    )
