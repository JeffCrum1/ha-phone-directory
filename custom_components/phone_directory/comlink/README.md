# Comlink

Comlink is the output engine for the Phone Directory integration.

Its job is simple:

> Take the phone directory maintained by Home Assistant and publish it to one or more external destinations.

Comlink is intentionally independent of Home Assistant. Home Assistant provides the directory data and configuration; Comlink handles the work of turning that data into whatever format or service an output requires.

## Architecture

The relationship between Home Assistant and Comlink is intentionally separated:

```text
Home Assistant
      │
      │ directory data
      │ output configuration
      ▼
   Comlink
      │
      ├── Grandstream
      ├── VoIP.ms
      ├── Debug
      └── future outputs
```

Home Assistant does not need to know how an output works.

Comlink does not need to know how Home Assistant works.

That separation is intentional.

## Outputs

Every output lives in its own directory under:

```text
comlink/outputs/
```

For example:

```text
comlink/
└── outputs/
    ├── debug/
    ├── grandstream/
    └── voipms/
```

An output package owns everything specific to that output:

* Its implementation
* Its configuration definition
* Its construction logic
* Its documentation

This keeps output-specific knowledge out of Comlink's core.

## Self-Describing Outputs

Each output package provides three things:

```text
OUTPUT_DEFINITION
OUTPUT_CLASS
create_output()
```

### `OUTPUT_DEFINITION`

`OUTPUT_DEFINITION` describes the output to the rest of Comlink.

It contains:

* `output_type` — the technical identifier used in configuration
* `label` — the human-readable name
* `fields` — the configuration fields required by the output

Each field describes:

* `key`
* `label`
* `type`
* `required`
* `secret`
* `default`

The definition is read-only.

Home Assistant can use this information to build its configuration forms without needing output-specific knowledge.

### `OUTPUT_CLASS`

`OUTPUT_CLASS` identifies the implementation class used by the output.

### `create_output()`

`create_output()` converts an `OutputConfig` into an instance of the output implementation.

The output package owns this conversion because the output package knows what its constructor requires.

## Output Discovery

Comlink does not maintain a central list of output types.

Instead, the output factory discovers packages under:

```text
comlink/outputs/
```

and asks each package whether it provides an `OUTPUT_DEFINITION`.

This means the core of Comlink does not contain code such as:

```python
if output_type == "grandstream":
```

or:

```python
if output_type == "voipms":
```

That is deliberate.

## Adding a New Output

Adding an output should normally require creating a new output package rather than modifying Comlink's core.

For example:

```text
comlink/outputs/my_output/
├── __init__.py
├── my_output.py
└── README.md
```

The package should provide:

```python
OUTPUT_DEFINITION
OUTPUT_CLASS
create_output()
```

The implementation should satisfy the output contract defined by Comlink.

Once the package exists, Comlink discovers it automatically.

Home Assistant should not require a code change simply because a new Comlink output was added.

This is one of the primary architectural goals of Comlink.

## Configuration

The configuration stored by Home Assistant identifies an output using an `output_id` and `output_type`, along with the fields required by that output.

For example:

```json
{
    "output_id": "example-id",
    "name": "House Phones",
    "output_type": "grandstream",
    "directory": "/config/www",
    "filename": "phonebook.xml"
}
```

The exact configuration fields are defined by the output's `OUTPUT_DEFINITION`.

## Output Documentation

Every output should have its own `README.md`.

The output README should explain:

* What the output does
* What its configuration fields mean
* Any defaults
* Any output-specific requirements
* Any external service or device requirements
* Any limitations or special behavior

The Comlink README explains **how outputs work**.

The individual output README explains **how that output works**.

Keeping those responsibilities separate makes the project easier to understand and extend.

## Design Goal

The goal of Comlink is not to predict every possible output.

The goal is to make adding the next output boring.

If someone wants to add another destination, they should be able to create an output package, describe its configuration, implement its publishing behavior, document it, and let Comlink discover it.

The core should not need to know its name.
