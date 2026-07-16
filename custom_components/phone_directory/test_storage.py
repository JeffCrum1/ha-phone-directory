import sys
import types


# Fake Home Assistant imports for standalone testing
homeassistant = types.ModuleType("homeassistant")
config_entries = types.ModuleType("homeassistant.config_entries")
core = types.ModuleType("homeassistant.core")


class ConfigEntry:
    pass


class HomeAssistant:
    pass


config_entries.ConfigEntry = ConfigEntry
core.HomeAssistant = HomeAssistant

sys.modules["homeassistant"] = homeassistant
sys.modules["homeassistant.config_entries"] = config_entries
sys.modules["homeassistant.core"] = core


from custom_components.phone_directory.comlink.storage import (
    DATA_FILE,
    load_contacts,
    add_contact,
    delete_contact,
    change_contact,
)


# Start clean
if DATA_FILE.exists():
    DATA_FILE.unlink()
    print(f"Deleted existing {DATA_FILE}")
else:
    print(f"No existing {DATA_FILE} found")


print()
print("Initial:")
print(load_contacts())


print()
print("Adding contacts...")

add_contact(
    "Jeff - Cell",
    "5551111111",
)

add_contact(
    "Son - Cell",
    "5552222222",
)

print(load_contacts())


print()
print("Changing Son - Cell to Son - Home...")

change_contact(
    "Son - Cell",
    "Son - Home",
    "5553333333",
)

print(load_contacts())


print()
print("Deleting Jeff - Cell...")

delete_contact(
    "Jeff - Cell",
)

print(load_contacts())
