import argparse
import sys

import bakrep.download


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
        help="A tsv with the datasets to download. The first column will be used as the id column."
    )
    input_group.add_argument(
        '-e', '--entries',
        help="""Comma separated list of entries to download"""
    )
    output_group = download_parser.add_argument_group("output")
    output_group.add_argument(
        '-d', '--directory',
        default="./",
        help="The directory where the datasets will be downloaded to. (default %(default)s)"
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
          Example: '-m tool:bakta,filetype:gff3'"""
    )
    download_parser.add_argument(
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
    main(sys.argv)
