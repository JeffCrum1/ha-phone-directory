from dataclasses import dataclass


@dataclass
class OutputConfig:
    """Configuration for a phone directory output."""

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
