from dataclasses import dataclass


@dataclass
class OutputConfig:
    """Configuration for a phone directory output."""

    output_type: str
    data: dict
