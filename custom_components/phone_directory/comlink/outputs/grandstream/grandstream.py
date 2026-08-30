import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom


LOGGER = logging.getLogger(__name__)


class GrandstreamOutput:
    """Grandstream pull-based output."""

    def __str__(self) -> str:
        return "Grandstream"

    def publish(self, contacts) -> None:
        """Handle a publish request for the Grandstream output."""

        LOGGER.debug(
            "Phone Directory: no publish for Grandstream; "
            "Grandstream retrieves the phonebook from the HTTP API",
        )

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

        pretty_xml = minidom.parseString(
            rough_xml,
        ).toprettyxml(
            indent="    ",
            encoding=None,
        )

        return '<?xml version="1.0" encoding="UTF-8"?>\n' + pretty_xml.split("\n", 1)[1]
