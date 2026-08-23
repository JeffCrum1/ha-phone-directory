import json
import logging
import urllib.parse
import urllib.request

from .storage import (
    get_phonebook_id,
    load_mappings,
    remove_phonebook_id,
    save_phonebook_id,
)


LOGGER = logging.getLogger(__name__)


class VoipmsApiError(Exception):
    """A VoIP.ms API error."""

    def __init__(
        self,
        status: str,
        message: str,
    ):
        """Initialize the error."""

        self.status = status
        self.message = message

        super().__init__(
            f"VoIP.ms API error: {status}: {message}",
        )


class VoipmsPhonebookNotFound(VoipmsApiError):
    """The requested VoIP.ms phonebook entry does not exist."""

    def __init__(
        self,
        message: str,
    ):
        """Initialize the error."""

        super().__init__(
            "invalid_phonebook",
            message,
        )


class VoipmsOutput:
    """Manage phone directory entries on VoIP.ms."""

    API_URL = "https://voip.ms/api/v1/rest.php"

    def __init__(
        self,
        output_id: str,
        api_username: str,
        api_password: str,
    ):
        """Initialize VoIP.ms output."""

        self.output_id = output_id
        self.api_username = api_username
        self.api_password = api_password

    def __str__(self) -> str:
        return "VoIP.ms"

    def publish(
        self,
        contacts,
    ) -> None:
        """Reconcile the HA phone directory with VoIP.ms."""

        LOGGER.debug(
            "Phone Directory: VoIP.ms publish starting with %s HA contacts",
            len(contacts),
        )

        mappings = load_mappings()

        voipms_ids = {}

        for contact_id, phonebook_id in mappings.items():
            if phonebook_id in voipms_ids:
                other_contact_id = voipms_ids[phonebook_id]

                raise VoipmsApiError(
                    "xref_integrity",
                    (
                        "CRITICAL: VoIP.ms xref integrity error: "
                        f"VoIP.ms phonebook ID {phonebook_id} is mapped to "
                        f"multiple HA contacts ({other_contact_id} and "
                        f"{contact_id}). Publishing has been aborted. "
                        "This is a program/data integrity error and must "
                        "be corrected before publishing can continue."
                    ),
                )

            voipms_ids[phonebook_id] = contact_id

        LOGGER.debug(
            "Phone Directory: VoIP.ms xref validation passed with %s mappings",
            len(mappings),
        )

        phonebooks = self._get_phonebook()

        contacts_by_id = {contact.contact_id: contact for contact in contacts}

        xref_by_contact_id = dict(mappings)

        phonebooks_by_id = {
            str(phonebook["phonebook"]): phonebook for phonebook in phonebooks
        }

        checked = 0
        matched = 0
        added = 0
        updated = 0
        recreated = 0
        deleted = 0
        unmapped_deleted = 0

        for contact in contacts:
            checked += 1

            phonebook_id = xref_by_contact_id.get(
                contact.contact_id,
            )

            if phonebook_id is None:
                LOGGER.debug(
                    "Phone Directory: VoIP.ms HA contact %s (%s) has no "
                    "xref mapping - adding to VoIP.ms",
                    contact.name,
                    contact.contact_id,
                )

                new_phonebook_id = self.add_contact(
                    contact,
                )

                xref_by_contact_id[contact.contact_id] = new_phonebook_id

                added += 1

                LOGGER.debug(
                    "Phone Directory: VoIP.ms HA contact %s (%s) added "
                    "as phonebook entry %s",
                    contact.name,
                    contact.contact_id,
                    new_phonebook_id,
                )

                continue

            phonebook = phonebooks_by_id.get(
                phonebook_id,
            )

            if phonebook is None:
                LOGGER.debug(
                    "Phone Directory: VoIP.ms HA contact %s (%s) maps to "
                    "phonebook entry %s, but the remote record does not "
                    "exist - recreating",
                    contact.name,
                    contact.contact_id,
                    phonebook_id,
                )

                new_phonebook_id = self.add_contact(
                    contact,
                )

                xref_by_contact_id[contact.contact_id] = new_phonebook_id

                recreated += 1

                LOGGER.debug(
                    "Phone Directory: VoIP.ms HA contact %s (%s) recreated "
                    "as phonebook entry %s; xref updated",
                    contact.name,
                    contact.contact_id,
                    new_phonebook_id,
                )

                continue

            remote_name = phonebook.get(
                "name",
                "",
            )
            remote_number = phonebook.get(
                "number",
                "",
            )

            if remote_name == contact.name and remote_number == contact.number:
                LOGGER.debug(
                    "Phone Directory: VoIP.ms HA contact %s (%s) matches "
                    "phonebook entry %s - no action",
                    contact.name,
                    contact.contact_id,
                    phonebook_id,
                )

                matched += 1

                continue

            LOGGER.debug(
                "Phone Directory: VoIP.ms HA contact %s (%s) differs "
                "from phonebook entry %s - updating",
                contact.name,
                contact.contact_id,
                phonebook_id,
            )

            self.change_contact(
                contact,
            )

            updated += 1

            LOGGER.debug(
                "Phone Directory: VoIP.ms phonebook entry %s updated "
                "for HA contact %s (%s)",
                phonebook_id,
                contact.name,
                contact.contact_id,
            )

        for contact_id, phonebook_id in list(xref_by_contact_id.items()):
            if contact_id in contacts_by_id:
                continue

            LOGGER.debug(
                "Phone Directory: VoIP.ms xref maps HA contact %s to "
                "phonebook entry %s, but the HA contact no longer exists "
                "- deleting remote record",
                contact_id,
                phonebook_id,
            )

            self._delete_phonebook(
                phonebook_id,
            )

            phonebooks_by_id.pop(
                phonebook_id,
                None,
            )

            remove_phonebook_id(
                contact_id,
            )

            del xref_by_contact_id[contact_id]

            deleted += 1

            LOGGER.debug(
                "Phone Directory: VoIP.ms remote phonebook entry %s "
                "deleted and xref mapping for HA contact %s removed",
                phonebook_id,
                contact_id,
            )

        for phonebook_id in list(phonebooks_by_id):
            if phonebook_id in xref_by_contact_id.values():
                continue

            LOGGER.debug(
                "Phone Directory: VoIP.ms phonebook entry %s has no "
                "xref mapping - deleting unmapped remote record",
                phonebook_id,
            )

            self._delete_phonebook(
                phonebook_id,
            )

            unmapped_deleted += 1

            LOGGER.debug(
                "Phone Directory: VoIP.ms unmapped phonebook entry %s deleted",
                phonebook_id,
            )

        LOGGER.debug(
            "Phone Directory: VoIP.ms reconciliation complete: "
            "checked=%s, matched=%s, added=%s, updated=%s, "
            "recreated=%s, deleted=%s, unmapped_deleted=%s",
            checked,
            matched,
            added,
            updated,
            recreated,
            deleted,
            unmapped_deleted,
        )

    def _get_phonebook(self) -> list[dict]:
        """Retrieve the complete VoIP.ms phonebook."""

        LOGGER.debug(
            "Phone Directory: VoIP.ms retrieving phonebook",
        )

        result = self._api_call(
            "getPhonebook",
        )

        phonebooks = result.get(
            "phonebooks",
            [],
        )

        if not isinstance(phonebooks, list):
            raise VoipmsApiError(
                "invalid_response",
                "VoIP.ms phonebook response did not contain a list of phonebooks",
            )

        LOGGER.debug(
            "Phone Directory: VoIP.ms retrieved %s phonebook entries",
            len(phonebooks),
        )

        return phonebooks

    def add_contact(
        self,
        contact,
    ) -> str:
        """Add a contact to VoIP.ms."""

        LOGGER.debug(
            "Phone Directory: VoIP.ms adding contact %s (%s)",
            contact.name,
            contact.contact_id,
        )

        result = self._api_call(
            "setPhonebook",
            phonebook="",
            name=contact.name,
            number=contact.number,
        )

        phonebook_id = str(
            result["phonebook"],
        )

        LOGGER.debug(
            "Phone Directory: VoIP.ms created phonebook entry %s for contact %s",
            phonebook_id,
            contact.contact_id,
        )

        save_phonebook_id(
            contact.contact_id,
            phonebook_id,
        )

        LOGGER.debug(
            "Phone Directory: VoIP.ms saved phonebook mapping for contact %s",
            contact.contact_id,
        )

        return phonebook_id

    def change_contact(
        self,
        contact,
    ) -> None:
        """Change a contact on VoIP.ms."""

        phonebook_id = get_phonebook_id(
            contact.contact_id,
        )

        if phonebook_id is None:
            LOGGER.debug(
                "Phone Directory: VoIP.ms no phonebook mapping for contact %s; "
                "adding contact",
                contact.contact_id,
            )

            self.add_contact(
                contact,
            )

            return

        LOGGER.debug(
            "Phone Directory: VoIP.ms changing contact %s using phonebook " "entry %s",
            contact.contact_id,
            phonebook_id,
        )

        try:
            self._api_call(
                "setPhonebook",
                phonebook=phonebook_id,
                name=contact.name,
                number=contact.number,
            )

        except VoipmsPhonebookNotFound:
            LOGGER.debug(
                "Phone Directory: VoIP.ms phonebook entry %s is missing "
                "for contact %s; adding contact",
                phonebook_id,
                contact.contact_id,
            )

            self.add_contact(
                contact,
            )

            return

        LOGGER.debug(
            "Phone Directory: VoIP.ms changed phonebook entry %s for contact %s",
            phonebook_id,
            contact.contact_id,
        )

    def delete_contact(
        self,
        contact,
    ) -> None:
        """Delete a contact from VoIP.ms."""

        phonebook_id = get_phonebook_id(
            contact.contact_id,
        )

        if phonebook_id is None:
            LOGGER.debug(
                "Phone Directory: VoIP.ms no phonebook mapping for deleted "
                "contact %s",
                contact.contact_id,
            )

            return

        self._delete_phonebook(
            phonebook_id,
        )

        remove_phonebook_id(
            contact.contact_id,
        )

        LOGGER.debug(
            "Phone Directory: VoIP.ms removed phonebook mapping for contact %s",
            contact.contact_id,
        )

    def _delete_phonebook(
        self,
        phonebook_id: str,
    ) -> None:
        """Delete a VoIP.ms phonebook entry by ID."""

        LOGGER.debug(
            "Phone Directory: VoIP.ms deleting phonebook entry %s",
            phonebook_id,
        )

        try:
            self._api_call(
                "delPhonebook",
                phonebook=phonebook_id,
            )

        except VoipmsPhonebookNotFound:
            LOGGER.debug(
                "Phone Directory: VoIP.ms phonebook entry %s is already missing",
                phonebook_id,
            )

    def _api_call(
        self,
        method: str,
        **params,
    ) -> dict:
        """Call the VoIP.ms API."""

        params.update(
            {
                "api_username": self.api_username,
                "api_password": self.api_password,
                "method": method,
            }
        )

        url = self.API_URL + "?" + urllib.parse.urlencode(params)

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
            },
        )

        LOGGER.debug(
            "Phone Directory: VoIP.ms API request starting: %s",
            method,
        )

        with urllib.request.urlopen(request) as response:
            data = response.read().decode("utf-8")

        LOGGER.debug(
            "Phone Directory: VoIP.ms API response received: %s",
            method,
        )

        result = json.loads(data)

        if not result or result.get("status") != "success":
            status = result.get(
                "status",
                "unknown",
            )
            message = result.get(
                "message",
                "Unknown VoIP.ms API error",
            )

            if status == "invalid_phonebook":
                raise VoipmsPhonebookNotFound(
                    message,
                )

            raise VoipmsApiError(
                status,
                message,
            )

        return result
