"""Persistent state for the VoIP.ms output."""

import json
from pathlib import Path


DATA_DIR = Path("/config/phone_directory_data")
DATA_FILE = DATA_DIR / "voipms.json"


def load_mappings() -> dict[str, str]:
    """Load HA contact ID to VoIP.ms phonebook ID mappings."""

    if not DATA_FILE.exists():
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        return {}

    mappings = data.get("contacts", {})

    if not isinstance(mappings, dict):
        return {}

    return {
        str(contact_id): str(phonebook_id)
        for contact_id, phonebook_id in mappings.items()
    }


def save_mappings(mappings: dict[str, str]) -> None:
    """Save HA contact ID to VoIP.ms phonebook ID mappings."""

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "contacts": mappings,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )


def get_phonebook_id(contact_id: str) -> str | None:
    """Return the VoIP.ms phonebook ID for an HA contact."""

    mappings = load_mappings()

    return mappings.get(contact_id)


def save_phonebook_id(
    contact_id: str,
    phonebook_id: str,
) -> None:
    """Save the VoIP.ms phonebook ID for an HA contact."""

    mappings = load_mappings()

    mappings[contact_id] = phonebook_id

    save_mappings(mappings)


def remove_phonebook_id(contact_id: str) -> None:
    """Remove the VoIP.ms phonebook ID for an HA contact."""

    mappings = load_mappings()

    if contact_id not in mappings:
        return

    del mappings[contact_id]

    save_mappings(mappings)
