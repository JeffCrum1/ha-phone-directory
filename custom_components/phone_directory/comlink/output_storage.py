import json
from dataclasses import asdict
from pathlib import Path

from .output_models import OutputConfig

DATA_FILE = Path("/config/outputs.json")


def load_outputs() -> list[OutputConfig]:
    """Load all output configurations from storage."""

    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [OutputConfig(**item) for item in data]


def save_outputs(outputs: list[OutputConfig]) -> None:
    """Save all output configurations to storage."""

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [asdict(output) for output in outputs],
            f,
            indent=2,
            ensure_ascii=False,
        )


def add_output(
    output_id: str,
    output_type: str,
    data: dict,
) -> None:
    """Add a new output configuration."""

    outputs = load_outputs()

    if any(output.output_id == output_id for output in outputs):
        raise ValueError(f"Output already exists: {output_id}")

    outputs.append(
        OutputConfig(
            output_id=output_id,
            output_type=output_type,
            data=data,
        )
    )

    save_outputs(outputs)


def delete_output(output_id: str) -> None:
    """Delete an output configuration."""

    outputs = load_outputs()

    outputs = [output for output in outputs if output.output_id != output_id]

    save_outputs(outputs)


def change_output(
    old_output_id: str,
    new_output_id: str,
    output_type: str,
    data: dict,
) -> None:
    """Change an output configuration."""

    outputs = load_outputs()

    for output in outputs:
        if output.output_id == old_output_id:

            if new_output_id != old_output_id and any(
                o.output_id == new_output_id for o in outputs
            ):
                raise ValueError(f"Output already exists: {new_output_id}")

            output.output_id = new_output_id
            output.output_type = output_type
            output.data = data

            save_outputs(outputs)
            return

    raise ValueError(f"Output not found: {old_output_id}")
