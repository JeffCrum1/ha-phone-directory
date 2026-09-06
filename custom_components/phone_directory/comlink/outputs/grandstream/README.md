# Grandstream Output

The Grandstream output provides the Phone Directory to Grandstream phones through an HTTP endpoint.

Unlike a traditional push-based output, the Grandstream output does not write a phonebook file to disk and does not publish the directory to the phone.

Instead, **the Grandstream phone pulls the current phonebook from Home Assistant when it requests it.**

## How It Works

The relationship looks like this:

```text
Home Assistant
      │
      │ current Phone Directory
      ▼
   Comlink
      │
      │ HTTP endpoint
      ▼
 Grandstream
```

The Grandstream phone is responsible for requesting the phonebook.

When the phone makes the request, Comlink:

1. Authenticates the request using the configured Grandstream credentials.
2. Loads the current Phone Directory.
3. Generates Grandstream-compatible XML.
4. Returns the XML directly to the phone.

There is no intermediate `phonebook.xml` file.

There is no `/local` path.

There is no separate web server.

The phone receives the current directory directly from Home Assistant.

## Configuration

The Grandstream output requires three settings:

* **User ID** — Username Grandstream uses when requesting the phonebook.
* **Password** — Password Grandstream uses when requesting the phonebook.
* **Server Path** — The HTTP server and path Grandstream uses to retrieve the phonebook.

The endpoint is:

```text
/api/phone_directory/<output_id>/phonebook.xml
```

The `<output_id>` is the unique identifier assigned to this output configuration.

The output ID is intentionally part of the URL. Because it is a generated identifier rather than a human-readable name, it makes the endpoint difficult to discover by simply guessing URLs.

This is **obscurity, not authentication**. The endpoint still requires valid credentials.

The complete Server Path therefore points to the Home Assistant instance running Phone Directory.

The Grandstream configuration should use the Server Path without an HTTP or HTTPS scheme when required by the Grandstream phone's phonebook settings.

## Authentication

The Grandstream phone authenticates to the endpoint using **HTTP Basic Authentication**.

The User ID and Password configured in Phone Directory must match the credentials configured on the Grandstream phone.

These credentials are specific to this Phone Directory output.

Home Assistant user accounts and Home Assistant access tokens are not used.

If the credentials are incorrect, the endpoint returns:

```text
401 Unauthorized
```

The combination of a non-guessable output-specific URL and HTTP authentication provides two separate barriers:

1. The endpoint must be known.
2. Valid credentials must be supplied.

The output ID should not be considered a secret, and it should not be relied upon as the security mechanism.

## Phonebook Format

Phone Directory generates the phonebook in the XML format expected by Grandstream phones.

The generated phonebook contains the current contacts from Home Assistant.

Each contact is represented with its name and telephone number.

The XML is generated when Grandstream requests it, so the response reflects the current Phone Directory state at the time of the request.

## Synchronization Model

The Grandstream output is **pull-based**.

Grandstream initiates synchronization by requesting the phonebook.

This is different from a push-based output such as a service where Phone Directory must actively send changes to the destination.

The important distinction is:

> **Home Assistant remains the source of truth. Grandstream simply retrieves the current representation of that state.**

If the Phone Directory changes, there is nothing that needs to be pushed to Grandstream.

The next time Grandstream retrieves the phonebook, it receives the updated directory.

## Design

The Grandstream output follows the Comlink output interface.

It receives the current directory when Comlink invokes the output, but a normal publish operation does not send anything to Grandstream.

Instead, the output exposes an HTTP resource that Comlink's HTTP layer makes available through Home Assistant.

This keeps the Grandstream-specific behavior inside the Grandstream output while keeping Home Assistant HTTP handling in Comlink.

## Requirements

The Grandstream phone must be able to reach the Home Assistant HTTP server over the network.

The phone must also be configured to retrieve its phonebook from the Server Path using the same User ID and Password configured for the Grandstream output.

The exact phone menu names and phonebook refresh behavior may vary between Grandstream models and firmware versions.

## Troubleshooting

### 401 Unauthorized

The phone reached the endpoint, but authentication failed.

Check that the Grandstream User ID and Password exactly match the credentials configured in the Phone Directory Grandstream output.

### The phone cannot connect

Verify that:

* The Grandstream can reach Home Assistant.
* The Server Path points to the correct Home Assistant address.
* The Home Assistant HTTP port is reachable from the phone.
* The Server Path is configured in the format expected by the Grandstream model.

### The phonebook is not updating

Remember that Grandstream is **pulling** the phonebook.

Phone Directory does not push an updated file to the phone.

The phone must request the phonebook again for changes to appear. Check the Grandstream phone's phonebook download or refresh settings if an update is not appearing.

## Summary

The Grandstream output is intentionally simple:

```text
Phone Directory
      │
      ▼
   Comlink
      │
      │ HTTP GET
      ▼
 Grandstream
```

Home Assistant owns the directory.

Comlink provides the connection between the directory and Grandstream.

Grandstream asks for the current phonebook when it needs it.

No generated file is stored on disk, and no separate web server is required.
