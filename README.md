# python-openca-tools

Python client and command-line tool for processing
[Open Government Canada](https://open.canada.ca/en) datasets.

## Getting started

### Installation
```sh
python -m pip install git+https://github.com/ely-as/python-openca-tools
```

### Usage
For example, to convert the SDMX XML files in
[98-400-X2016361](https://open.canada.ca/data/en/dataset/37f42796-9926-442c-a319-fecab5030388)
to a CSV and JSON file:
```sh
openca_tools csvify Generic_98-400-X2016361.xml
```

Currently this is the only command available in the client. It creates four new
files:
- A CSV file containing each data point.
- A JSON file containing mappings between the codes used in the CSV file and
  their English or French labels. Also contains the line length of the CSV file
  that was generated.
- Two SHA-256 checksum sidecar files (one for each of the above files).

## Why

The datasets available on [open.canada.ca](https://open.canada.ca/en) are
provided in SDMX XML format. They can be difficult to load or process
programmatically due to their large uncompressed size and the need for the XML
to be parsed. For example, converting
[98-400-X2016361](https://open.canada.ca/data/en/dataset/37f42796-9926-442c-a319-fecab5030388)
from SDMX XML to CSV reduces the uncompressed file size from 44G to 1.4G.

## Other resources

- [GitHub - Open Government Initiative - Initiative sur le gouvernement ouvert](https://github.com/open-data)
