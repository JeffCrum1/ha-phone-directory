# Debug Output

The Debug output is a development and testing output.

It does not publish the Phone Directory to an external device or service.

Instead, it records information about the directory received by the output through the logging system.

## Purpose

Debug exists to make the Comlink output pipeline easy to test without requiring an external destination.

It can be used to verify that:

* An output is discovered correctly
* An output can be configured
* Comlink can construct the output
* Contacts reach the output
* The publish operation completes successfully

## Configuration

Debug does not currently require any output-specific configuration fields.

The configured output name and ID are used to identify the output in log messages.

## Publishing

When Comlink publishes to the Debug output, it logs:

* The output name
* The output ID
* The number of contacts received
* The contacts received
* A successful publication message

No external data is transmitted.

No files are created.

No external service is contacted.

## Intended Use

Debug is primarily a development and troubleshooting tool.

It provides a safe destination for testing changes to the Comlink pipeline before testing against a real phone, service, or other external destination.

## Notes

Debug is intentionally implemented using the same output contract as production outputs.

That makes it useful for testing Comlink itself as well as providing a simple reference implementation for developers adding new outputs.
