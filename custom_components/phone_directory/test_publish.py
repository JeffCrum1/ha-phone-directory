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


from custom_components.phone_directory.comlink.storage import load_contacts
from custom_components.phone_directory.comlink.publisher import publish_contacts


print()
print("Loading contacts...")

contacts = load_contacts()

print("Loaded contacts:")
print(contacts)


print()
print("Publishing to configured outputs...")

publish_contacts(contacts)


print()
print("Done")
