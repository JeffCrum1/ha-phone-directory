import json
import urllib.parse
import urllib.request


class VoipmsOutput:
    """Publish phone directory to VoIP.ms."""

    API_URL = "https://voip.ms/api/v1/rest.php"

    def __init__(
        self,
        api_username: str,
        api_password: str,
    ):
        """Initialize VoIP.ms output."""

        self.api_username = api_username
        self.api_password = api_password

    def __str__(self) -> str:
        return "VoIP.ms"

    def publish(self, contacts) -> None:
        """Replace the VoIP.ms phonebook with current contacts."""

        existing = self._get_phonebook()

        for entry in existing:
            self._delete_phonebook(
                entry["phonebook"],
            )

        for contact in contacts:
            self._create_phonebook_entry(
                contact.name,
                contact.number,
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

        with urllib.request.urlopen(request) as response:
            data = response.read().decode("utf-8")

        result = json.loads(data)

        if result.get("status") != "success":
            raise RuntimeError(f"VoIP.ms API error: {result.get('status')}")

    def _get_phonebook(self) -> list[dict]:
        """Retrieve current VoIP.ms phonebook entries."""

        result = self._api_call(
            "getPhonebook",
        )

        return result.get(
            "phonebooks",
            [],
        )

    def _create_phonebook_entry(
        self,
        name: str,
        number: str,
    ) -> None:
        """Create a VoIP.ms phonebook entry."""

        self._api_call(
            "setPhonebook",
            phonebook="",
            name=name,
            number=number,
        )

    def _delete_phonebook(
        self,
        phonebook_id: str,
    ) -> None:
        """Delete a VoIP.ms phonebook entry."""

        self._api_call(
            "delPhonebook",
            phonebook=phonebook_id,
        )
