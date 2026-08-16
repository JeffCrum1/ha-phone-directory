import importlib
import pkgutil

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
