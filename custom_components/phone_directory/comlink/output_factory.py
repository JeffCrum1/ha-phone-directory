import importlib
import pkgutil

from homeassistant.core import HomeAssistant

from . import outputs
from .output_models import OutputConfig, OutputDefinition


def get_output_definitions() -> list[OutputDefinition]:
    """Discover and return all available output definitions."""

    definitions = []

    for module_info in pkgutil.iter_modules(outputs.__path__):
        if module_info.name.startswith("_"):
            continue

        module = importlib.import_module(
            f"{outputs.__name__}.{module_info.name}",
        )

        definition = getattr(
            module,
            "OUTPUT_DEFINITION",
            None,
        )

        if definition is not None:
            definitions.append(definition)

    return sorted(
        definitions,
        key=lambda definition: definition.label.lower(),
    )


async def async_get_output_definitions(
    hass: HomeAssistant,
) -> list[OutputDefinition]:
    """Discover output definitions without blocking Home Assistant."""

    return await hass.async_add_executor_job(
        get_output_definitions,
    )


def create_output(config: OutputConfig):
    """Create an output instance from configuration."""

    module = importlib.import_module(
        f"{outputs.__name__}.{config.output_type}",
    )

    create = getattr(
        module,
        "create_output",
        None,
    )

    if create is None:
        raise ValueError(
            f"Output does not provide a create_output function: "
            f"{config.output_type}",
        )

    return create(config)


async def async_create_output(
    hass: HomeAssistant,
    config: OutputConfig,
):
    """Create an output instance without blocking Home Assistant."""

    return await hass.async_add_executor_job(
        create_output,
        config,
    )
