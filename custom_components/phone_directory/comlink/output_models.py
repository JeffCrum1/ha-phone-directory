from dataclasses import dataclass


@dataclass
class OutputConfig:
    """Configuration for a phone directory output."""

    output_id: str
    output_type: str
    data: dict
