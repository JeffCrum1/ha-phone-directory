# Onscreen

The `onscreen/` package provides the Home Assistant UI used to manage the Phone Directory.

It is intentionally a thin presentation layer. The Phone Directory remains the source of truth for contacts and their lifecycle; `onscreen/` provides the screens and interactions that let a user view, add, edit, and delete those contacts.

## Responsibilities

* Display the current Phone Directory.
* Provide the user interface for adding contacts.
* Provide the user interface for editing contacts.
* Provide confirmation before deleting contacts.
* Provide an explicit **Publish** action.
* Send contact changes back through the Phone Directory rather than maintaining a separate copy of the directory.

## Publishing

Changing a contact does **not** automatically publish the directory.

The onscreen UI provides an explicit **Publish** action. When the user publishes, the Phone Directory sends the **complete current directory** to Comlink.

Push-type outputs receive that complete snapshot and send it to their external destination. The output determines what publishing the snapshot means for that destination.

Pull-type outputs are different. They do not receive the publish operation; instead, the external system reaches into the Phone Directory through the interface provided by that output.

The onscreen code does not need to know which outputs are push or pull. It simply provides the user-controlled Publish action.

## Boundary

The onscreen UI does **not** define a second contact model or maintain its own directory state.

The core Phone Directory owns universally meaningful contact information:

* Name
* Phone number

Output-specific information belongs to the output that needs it, not to the onscreen contact model.

This keeps the UI simple for the household while leaving the architecture open for outputs that may eventually require additional information of their own.

## Design

The UI is intended for normal Home Assistant use, not as an administration interface for Comlink internals.

A user should be able to manage the Phone Directory without knowing how Comlink synchronizes its outputs.

The goal is simple:

**Manage the directory on screen. Publish it when you're ready. Let Comlink handle the rest.**
