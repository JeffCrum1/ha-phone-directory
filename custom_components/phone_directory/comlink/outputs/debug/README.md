# Debug Output

The Debug output is a development and troubleshooting output for Comlink.

It does not publish data to an external destination. Instead, it receives the same contact data that the other configured outputs receive and writes that data to the Home Assistant log.

## Purpose

The Debug output provides a simple way to see exactly what Comlink is passing to an output without inspecting files, APIs, or external devices.

When debug logging is enabled for the Phone Directory integration, the Debug output logs:

- The Debug output name
- The output ID
- The number of contacts received
- The complete list of contacts
- Confirmation that publishing completed successfully

The Debug output uses normal `DEBUG` logging and relies on Home Assistant's built-in integration debug logging.

## Using the Debug Output

The Debug output can remain configured permanently.

When troubleshooting the Phone Directory integration:

1. Enable debug logging for the Phone Directory integration in Home Assistant.
2. Perform the operation being tested.
3. Review the Home Assistant log or provide the relevant log output for troubleshooting.
4. Disable debug logging when finished.

There is no need to add or remove the Debug output when troubleshooting.

When debug logging is disabled, the Debug output produces no log messages.

## Design

The Debug output follows the same Comlink output interface as production outputs such as Grandstream and VoIP.ms.

It receives the current list of `Contact` objects through:

`publish(contacts)`

This makes it useful for verifying the complete publishing pipeline:

**Phone Directory storage → Coordinator → Comlink publisher → OutputManager → Debug output**

The Debug output does not modify contacts and does not affect other outputs.

Production outputs are completely unaware of whether a Debug output is configured. The Debug output is simply another Comlink output that receives the same published data.