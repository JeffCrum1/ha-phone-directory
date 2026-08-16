# VoIP.ms Output

The VoIP.ms output publishes the Phone Directory directly to the VoIP.ms phonebook service through the VoIP.ms REST API.

## Configuration

The VoIP.ms output requires two configuration fields.

### API Username

The API username for the VoIP.ms account.

### API Password

The API password for the VoIP.ms account.

The password is treated as a secret configuration value.

## Publishing

When the Phone Directory is published, the output:

1. Retrieves the existing VoIP.ms phonebook entries.
2. Removes the existing entries.
3. Creates new entries from the current Phone Directory.

This makes the Phone Directory the source of truth.

The output does not attempt to merge the Home Assistant directory with independently maintained VoIP.ms entries.

## Requirements

A VoIP.ms account with API access is required.

The credentials configured for the output must have permission to manage the VoIP.ms phonebook.

Internet access is required when publishing.

## Errors

API failures are reported back through the Comlink output pipeline.

The output does not silently treat an API failure as a successful publication.

## Notes

The VoIP.ms API details are intentionally contained within this output.

Neither Home Assistant nor Comlink's core needs to know how the VoIP.ms API works.

If the VoIP.ms API changes, the VoIP.ms output should be the only part of Comlink that normally needs to change.
