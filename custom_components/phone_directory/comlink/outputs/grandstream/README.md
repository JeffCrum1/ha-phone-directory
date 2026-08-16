# Grandstream Output

The Grandstream output publishes the Phone Directory as a Grandstream-compatible XML phonebook.

It generates an XML file containing the current directory contacts.

## Configuration

The Grandstream output currently has two configuration fields.

### Directory

The directory where the phonebook file will be written.

Example:

```text
/config/www
```

The directory is created automatically if it does not already exist.

### Filename

The name of the generated phonebook file.

The default is:

```text
phonebook.xml
```

If the filename is left at its default, a configuration such as:

```text
Directory: /config/www
Filename: phonebook.xml
```

produces:

```text
/config/www/phonebook.xml
```

The filename is configurable even though the current Grandstream setup normally uses `phonebook.xml`. This allows for future Grandstream models or configurations that may use a different filename.

## Publishing

Whenever the directory is published, Comlink generates a new XML document and writes it to the configured destination.

The output creates the destination directory when necessary.

## XML Format

The generated document uses the Grandstream `AddressBook` format.

Each Phone Directory contact is represented as a Grandstream contact with:

* First name
* Last name
* Ringtone
* Phone number

The current implementation writes phone numbers with a leading `1`.

## Requirements

The Grandstream phone or phones must be configured to retrieve the generated XML phonebook from the location provided by this output.

The Grandstream device configuration is outside the responsibility of Comlink.

## Notes

This output is intentionally responsible only for generating and publishing the Grandstream phonebook.

Home Assistant does not need to know anything about the Grandstream XML format.
