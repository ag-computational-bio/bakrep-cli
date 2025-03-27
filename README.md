# BakRep CLI - genome download tool

BakRep-CLI is a commandline tool to batch download genomic data (genomes, annotation, metadata) from BakRep to your computer.

## Usage

The CLI allows you to download BakRep datasets to a directory on your computer.

```txt
usage: bakrep download [-h] [-t TSV] [-e ENTRIES] [-d DIRECTORY] [-F] [-m FILTERS] [-r]

optional arguments:
  -h, --help            show this help message and exit

input:
  -t TSV, --tsv TSV     A tsv with the datasets ids to download. The dataset ids are extracted from the first column.
  -e ENTRIES, --entries ENTRIES
                        Comma separated list of dataset ids to download

output:
  -d DIRECTORY, --directory DIRECTORY
                        The target directory for the datasets. The datasets will be saved in group directories to avoid too many elements in a single directory. (default
                        ./)
  -F, --flat            Save all datasets to the download directory without any group directories. (default=off)

filters:
  -m FILTERS, --match FILTERS
                        Only download result files that match the attribute-filter. Can be provided multiple times. Example: '-m tool:bakta,filetype:gff3'. Currently
                        known attributes and values are: tool:bakta|checkm2|gtdbtk|assemblyscan, filetype:json|ffn|faa|gff3|gbff, type: qc|annotation|taxonomy

download:
  -r, --restart         Do not resume previous download, but download everything again.
```

## Getting started for development

Python dependency: >=3.9

Setup a virtualenv for development and install it in editable mode

```sh
# install in development environment
virtualenv --python=python3 venv; source venv/bin/activate;
pip3 install -e .

# Run unit tests
python -m unittest  -b
```
