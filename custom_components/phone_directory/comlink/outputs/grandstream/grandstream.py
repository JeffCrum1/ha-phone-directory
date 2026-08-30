"""Grandstream Comlink output."""

import logging
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

from aiohttp import BasicAuth
from aiohttp import web

from ...output_models import OutputConfig


LOGGER = logging.getLogger(__name__)


class GrandstreamOutput:
    """Grandstream pull-based output."""

    def __init__(self, config: OutputConfig) -> None:
        """Initialize the Grandstream output."""

        self.config = config

        self.http_path = f"/api/phone_directory/{config.output_id}/phonebook.xml"

        self.http_content_type = "application/xml"

    def __str__(self) -> str:
        return "Grandstream"

    def publish(self, contacts) -> None:
        """Handle a publish request for the Grandstream output."""

        LOGGER.debug(
            "Phone Directory: no publish for Grandstream; "
            "Grandstream retrieves the phonebook from the HTTP API",
        )

    def authenticate(self, request: web.Request) -> bool:
        """Authenticate an HTTP request using Grandstream credentials."""

        userid = self.config.data.get("userid")
        password = self.config.data.get("password")

        if not userid or not password:
            LOGGER.error(
                "Phone Directory: Grandstream output is missing " "HTTP credentials",
            )
            return False

        try:
            auth = BasicAuth.decode(
                request.headers.get("Authorization", ""),
            )
        except ValueError:
            return False

        return auth.login == userid and auth.password == password

    def render(self, contacts) -> str:
        """Generate Grandstream XML from contacts."""

        root = ET.Element("AddressBook")

        for contact in contacts:
            contact_elem = ET.SubElement(
                root,
                "Contact",
            )

            ET.SubElement(
                contact_elem,
                "FirstName",
            ).text = contact.name

            ET.SubElement(
                contact_elem,
                "LastName",
            ).text = ""

            ET.SubElement(
                contact_elem,
                "Ringtone",
            ).text = "0"

            phone = ET.SubElement(
                contact_elem,
                "Phone",
            )

            ET.SubElement(
                phone,
                "phonenumber",
            ).text = (
                "1" + contact.number
            )

        rough_xml = ET.tostring(
            root,
            encoding="unicode",
        )

        pretty_xml = parseString(
            rough_xml,
        ).toprettyxml(
            indent="    ",
            encoding=None,
        )

        return '<?xml version="1.0" encoding="UTF-8"?>\n' + pretty_xml.split("\n", 1)[1]
