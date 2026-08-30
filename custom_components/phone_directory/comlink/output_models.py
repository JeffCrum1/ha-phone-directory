from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class OutputField:
    """Describe a configuration field for an output."""

    key: str
    label: str
    type: str
    required: bool = True
    secret: bool = False
    default: Any = None


@dataclass(frozen=True)
class OutputDefinition:
    """Describe an available Comlink output."""

    output_type: str
    label: str
    fields: tuple[OutputField, ...] = ()
    get_default: Callable[[Any], dict[str, Any]] | None = None


@dataclass(frozen=True)
class OutputConfig:
    """Configured output."""

    output_id: str
    output_type: str
    data: dict

    @classmethod
    def from_dict(cls, config: dict) -> "OutputConfig":
        """Create an OutputConfig from configuration data."""

        return cls(
            output_id=config["output_id"],
            output_type=config["output_type"],
            data=config,
        )
