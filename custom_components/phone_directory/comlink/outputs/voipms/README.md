# VoIP.ms Output

The VoIP.ms output keeps the VoIP.ms phonebook synchronized with the Phone Directory maintained by Home Assistant.

VoIP.ms is a **push-based** output.

When Phone Directory publishes the current directory, Comlink compares that desired state with the current VoIP.ms phonebook and makes the necessary changes.

The output does **not** simply delete the VoIP.ms phonebook and rebuild it.

## How It Works

The relationship looks like this:

```text
Home Assistant
      │
      │ current Phone Directory
      ▼
   Comlink
      │
      │ VoIP.ms API
      ▼
   VoIP.ms
```

When the Phone Directory is published, the VoIP.ms output:

1. Retrieves the current VoIP.ms phonebook.
2. Loads the persistent relationship between Home Assistant contacts and VoIP.ms phonebook entries.
3. Validates that relationship.
4. Compares the current Phone Directory with the VoIP.ms phonebook.
5. Adds missing entries.
6. Updates entries that have changed.
7. Recreates entries that disappeared from VoIP.ms.
8. Removes entries that should no longer exist.
9. Updates the persistent relationships as necessary.

The result is that the VoIP.ms phonebook is brought into agreement with the current Phone Directory.

## Configuration

The VoIP.ms output requires two settings:

* **API Username** — API username for the VoIP.ms account.
* **API Password** — API password for the VoIP.ms account.

The API password is stored as a secret configuration value.

A VoIP.ms account with API access and permission to manage the phonebook is required.

## Synchronization Model

The VoIP.ms output is **push-based**.

Phone Directory initiates synchronization by publishing the current directory to the output.

Push describes **who initiates synchronization**. It does not change where the directory comes from.

Home Assistant remains the source of truth.

The output receives the complete current directory and determines what the VoIP.ms phonebook should look like.

## Reconciliation

The output does not depend on knowing what changed since the previous publication.

Instead, each publication starts with two states:

* The complete current Phone Directory from Home Assistant
* The current phonebook retrieved from VoIP.ms

The output reconciles those states.

This means the synchronization can correct external changes made directly in VoIP.ms.

For example, if a VoIP.ms phonebook entry is manually changed, the next publication will restore it to the name and number defined by Home Assistant.

If an entry is manually deleted from VoIP.ms, the next publication recreates it.

If an entry exists in VoIP.ms but does not belong to the Phone Directory, it is removed.

This makes the synchronization **self-healing rather than event forwarding**.

## Contact Relationships

VoIP.ms assigns each phonebook entry its own `phonebook_id`.

Phone Directory contacts have their own `contact_id`.

The VoIP.ms output maintains a persistent relationship between those two identifiers:

```text
Home Assistant contact_id
            │
            │ maps to
            ▼
VoIP.ms phonebook_id
```

The mapping allows the output to recognize an existing VoIP.ms entry as the entry belonging to a particular Home Assistant contact.

The mapping is stored persistently in:

```text
/config/phone_directory_data/voipms.json
```

This relationship is destination-specific state owned by the VoIP.ms output.

## Adding Contacts

When a Home Assistant contact does not have a VoIP.ms mapping, the output creates a new VoIP.ms phonebook entry.

VoIP.ms returns the new `phonebook_id`.

That ID is then stored as the mapping for the Home Assistant contact.

On subsequent publications, the output can identify the existing remote entry rather than creating another one.

## Updating Contacts

If a mapped VoIP.ms entry exists and its name and number already match the Home Assistant contact, nothing needs to be done.

If either value differs, the existing VoIP.ms entry is updated.

The relationship between the Home Assistant contact and the VoIP.ms `phonebook_id` remains unchanged.

Changing a contact does not create a new VoIP.ms entry simply because its name or number changed.

## Recreating Missing Entries

External state can change independently of Phone Directory.

If Phone Directory has a mapping for a contact, but the corresponding VoIP.ms phonebook entry no longer exists, the output treats that as recoverable drift.

It creates a new VoIP.ms entry and updates the mapping to the new `phonebook_id`.

The next publication therefore restores the missing entry without requiring manual repair.

## Deleting Contacts

When a Home Assistant contact is removed from the Phone Directory, its mapped VoIP.ms phonebook entry is removed as well.

After the remote entry is deleted, its persistent mapping is removed.

The relationship therefore disappears along with the contact.

## Unmapped VoIP.ms Entries

The VoIP.ms phonebook may contain entries that have no relationship to a Home Assistant contact.

Those entries are considered **orphaned remote records**.

Because Home Assistant is the source of truth, an unmapped VoIP.ms phonebook entry does not belong in the synchronized phonebook.

The output removes it during reconciliation.

This also means that manually adding an unrelated entry directly to the VoIP.ms phonebook will not make it part of the Phone Directory.

## State Validation

The output validates its internal contact-to-phonebook relationships before modifying VoIP.ms.

A VoIP.ms `phonebook_id` must not be mapped to more than one Home Assistant contact.

If the persistent relationship data contains a duplicate remote ID, publishing is aborted rather than attempting to guess which contact is correct.

This distinction is intentional:

> **External state is allowed to be wrong. Internal relationship state is not.**

Missing or changed VoIP.ms records can be repaired through reconciliation.

Corrupt relationship data must be corrected rather than silently guessed at.

## Requirements

The VoIP.ms output requires:

* A VoIP.ms account
* VoIP.ms API access
* An API username
* An API password
* Internet access from Home Assistant

The configured credentials must have permission to manage the VoIP.ms phonebook.

## Errors

VoIP.ms API failures are reported through the Comlink output pipeline.

A failed API operation is not silently treated as a successful publication.

The output also distinguishes a missing remote phonebook entry from a general API failure. A missing mapped entry is normal external drift and can be repaired by creating the entry again.

## Design

The VoIP.ms API implementation is contained entirely within the VoIP.ms output.

Comlink's core does not need to know how the VoIP.ms API works.

The output owns:

* API communication
* Remote phonebook reconciliation
* Contact-to-phonebook relationships
* Recovery from missing remote entries
* Removal of orphaned remote entries
* VoIP.ms-specific error handling

This keeps VoIP.ms-specific knowledge out of the rest of Phone Directory and Comlink.

## Summary

The VoIP.ms output is intentionally a **reconciliation engine**, not a file exporter and not a simple delete-and-rebuild operation.

```text
Phone Directory
      │
      │ complete current state
      ▼
   Comlink
      │
      │ reconcile
      ▼
   VoIP.ms
```

Home Assistant owns the directory.

Comlink provides the output framework.

VoIP.ms provides the destination.

The VoIP.ms output makes the destination match the current Phone Directory and repairs normal external drift along the way.
