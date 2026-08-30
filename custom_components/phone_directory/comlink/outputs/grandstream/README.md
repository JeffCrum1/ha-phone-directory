# Grandstream Output

The Grandstream output generates a Grandstream-compatible XML phonebook and writes it to the configured destination.

Grandstream reads the phonebook XML through a web link, so the output directory should be under Home Assistant's `/config/www` directory to make the generated `phonebook.xml` accessible over HTTP.

## Configuration

The Grandstream output requires:

- **Directory** — Directory where the phonebook XML file will be written.
- **Filename** — Name of the generated XML file.

The default filename is:

`phonebook.xml`

## Output

The generated file contains the current Phone Directory contacts in Grandstream's XML phonebook format.

The output creates the destination directory if it does not already exist.

## Design

The Grandstream output follows the Comlink output interface:

`publish(contacts)`

It receives the current list of `Contact` objects and generates the XML file from that data.

The output does not manage contacts or determine when publishing occurs. Those responsibilities belong to the Phone Directory integration and Comlink publishing pipeline.