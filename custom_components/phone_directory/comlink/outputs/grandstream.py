import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom


class GrandstreamOutput:
    """Generate and publish a Grandstream XML phonebook."""

    def __init__(self, filename: str):
        """Initialize the output."""
        self.filename = Path(filename)

    def publish(self, contacts) -> None:
        """Generate XML and write it to the destination file."""

        xml = self._generate_xml(contacts)

        self.filename.write_text(
            xml,
            encoding="utf-8",
        )

    def _generate_xml(self, contacts) -> str:
        """Generate Grandstream XML from contacts."""

        root = ET.Element("AddressBook")

        for contact in contacts:
            contact_elem = ET.SubElement(root, "Contact")

            ET.SubElement(contact_elem, "FirstName").text = contact.name
            ET.SubElement(contact_elem, "LastName").text = ""
            ET.SubElement(contact_elem, "Ringtone").text = "0"

            phone = ET.SubElement(contact_elem, "Phone")
            ET.SubElement(phone, "phonenumber").text = "1" + contact.number

        rough_xml = ET.tostring(root, encoding="unicode")

        pretty_xml = minidom.parseString(rough_xml).toprettyxml(
            indent="    ",
            encoding=None,
        )

        return '<?xml version="1.0" encoding="UTF-8"?>\n' + pretty_xml.split("\n", 1)[1]
