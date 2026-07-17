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


from custom_components.phone_directory.comlink.output_storage import (
    DATA_FILE,
    load_outputs,
    add_output,
    delete_output,
    change_output,
)


# Start clean
if DATA_FILE.exists():
    DATA_FILE.unlink()
    print(f"Deleted existing {DATA_FILE}")
else:
    print(f"No existing {DATA_FILE} found")


print()
print("Initial:")
print(load_outputs())


print()
print("Adding outputs...")

add_output(
    "grandstream-home",
    "grandstream",
    {
        "directory": "/config/www/grandstream/home",
    },
)

add_output(
    "grandstream-office",
    "grandstream",
    {
        "directory": "/config/www/grandstream/office",
    },
)

print(load_outputs())


print()
print("Changing grandstream-office to grandstream-shop...")

change_output(
    "grandstream-office",
    "grandstream-shop",
    "grandstream",
    {
        "directory": "/config/www/grandstream/shop",
    },
)

print(load_outputs())


print()
print("Deleting grandstream-home...")

delete_output(
    "grandstream-home",
)

print(load_outputs())


print()
print("Final file contents:")
print(DATA_FILE.read_text())
