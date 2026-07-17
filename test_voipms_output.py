import os
import sys
import types
from pathlib import Path


# Allow importing custom_components
sys.path.insert(
    0,
    str(Path(__file__).parent),
)


# Fake Home Assistant imports for standalone testing
homeassistant = types.ModuleType("homeassistant")
config_entries = types.ModuleType("homeassistant.config_entries")
core = types.ModuleType("homeassistant.core")


class ConfigEntry:
    pass


class HomeAssistant:
    pass


class ServiceCall:
    pass


config_entries.ConfigEntry = ConfigEntry
core.HomeAssistant = HomeAssistant
core.ServiceCall = ServiceCall


sys.modules["homeassistant"] = homeassistant
sys.modules["homeassistant.config_entries"] = config_entries
sys.modules["homeassistant.core"] = core


from custom_components.phone_directory.comlink.models import Contact
from custom_components.phone_directory.comlink.outputs.voipms import VoipmsOutput


API_USERNAME = os.environ["VOIPMS_API_USERNAME"]
API_PASSWORD = os.environ["VOIPMS_API_PASSWORD"]


print()
print("Creating test contacts...")

contacts = [
    Contact(
        name="Phone Directory Test 1",
        number="5551111111",
    ),
    Contact(
        name="Phone Directory Test 2",
        number="5552222222",
    ),
]


print("Contacts:")
print(contacts)


print()
print("Publishing to VoIP.ms...")

output = VoipmsOutput(
    API_USERNAME,
    API_PASSWORD,
)

output.publish(contacts)


print()
print("Done")
