import argparse
import sys

import bakrep.download


def entrypoint():
    if (len(sys.argv) > 1):
        main(sys.argv[1:])
    else:
        main(["--help"])


def main(argv):
    parser = argparse.ArgumentParser(
        add_help=True,
        prog='bakrep',
        description='A tool to download bakrep datasets')

    sub_parsers = parser.add_subparsers(title="actions", required=True, )
    download_parser = sub_parsers.add_parser('download')
    input_group = download_parser.add_argument_group("input", )
    input_group.add_argument(
        '-t', '--tsv',
        help="A tsv with the datasets ids to download. The dataset ids are extracted from the first column."
    )
    input_group.add_argument(
        '-e', '--entries',
        help="""Comma separated list of dataset ids to download"""
    )
    output_group = download_parser.add_argument_group("output")
    output_group.add_argument(
        '-d', '--directory',
        default="./",
        help="The target directory for the datasets. The datasets will be saved in group directories to avoid too many elements in a single directory. (default %(default)s)"
    )
    output_group.add_argument(
        '-F', '--flat',
        action="store_true",
        default=False,
        help="Save all datasets to the download directory without any group directories. (default=off)"
    )

    filters_group = download_parser.add_argument_group("filters")
    filters_group.add_argument(
        '-m', '--match',
        dest="filters",
        action="append",
        help="""Only download result files that match the attribute-filter. Can be provided multiple times.
          Example: '-m tool:bakta,filetype:gff3'.
          Currently known attributes and values are:
            tool:bakta|checkm2|gtdbtk|assemblyscan,
            filetype:json|ffn|faa|gff3|gbff,
            type: qc|annotation|taxonomy
          """
    )

    download_group = download_parser.add_argument_group("download")
    download_group.add_argument(
        '-r', '--restart',
        action="store_true",
        default=False,
        help="""Do not resume previous download, but download everything again."""
    )

    args = parser.parse_args(argv)

    check = bakrep.download.check_args(args)
    if not check is None:
        parser.error(check)
    bakrep.download.download(args)


if __name__ == "__main__":
    entrypoint()
