import sys
import types
from pathlib import Path


sys.path.insert(
    0,
    str(Path(__file__).parents[2]),
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


from custom_components.phone_directory.coordinator import publish_everything


print()
print("Publishing everything...")

publish_everything()


print()
print("Done")
