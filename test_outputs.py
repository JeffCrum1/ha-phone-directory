import sys
import types

# Fake enough Home Assistant modules for importing the integration
homeassistant = types.ModuleType("homeassistant")
config_entries = types.ModuleType("homeassistant.config_entries")
core = types.ModuleType("homeassistant.core")

config_entries.ConfigEntry = object
core.HomeAssistant = object

sys.modules["homeassistant"] = homeassistant
sys.modules["homeassistant.config_entries"] = config_entries
sys.modules["homeassistant.core"] = core

sys.path.insert(0, "./custom_components")

from phone_directory.storage import load_contacts
from phone_directory.outputs import grandstream


contacts = load_contacts()

output = grandstream.GrandstreamOutput("/tmp/phonebook.xml")

output.publish(contacts)

print("Phonebook written!")
