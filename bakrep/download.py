from pathlib import Path
from typing import List

from bakrep.model import BakrepDownloader, DownloadFailedException, DownloadSet


def check_args(args):
    # tsv or entries must be present
    if args.tsv is None and args.entries is None:
        return "at least one of --tsv and --entries is required"
    if not args.tsv is None:
        tsv_path = Path(args.tsv)
        if not tsv_path.exists():
            return "the tsv does not exist"
        if not tsv_path.is_file():
            return "the tsv is not a file"

    output_path = Path(args.directory)
    if (output_path.exists() and not output_path.is_dir()):
        return "The output directory is a file. Delete it or use another output path."
    return None


def _parse_entries(entries: str):
    ids = []
    s = entries.split(",")
    for e in s:
        id = e.strip()
        if len(id) > 0:
            ids.append(e)
    return ids


def _parse_id_from_tsv_line(line: str):
    if (line.startswith("#")):
        return None
    s = line.split("\t", 1)
    id = s[0].strip()
    if len(id) > 0:
        return id
    return None


def _parse_ids_from_tsv(tsv_path: str):
    ids = []
    with open(tsv_path, "r") as tsv:
        for l in tsv:
            id = _parse_id_from_tsv_line(l)
            if not id is None:
                ids.append(id)
    return ids


def _parse_filters(filters: List[str]):
    parsed: List[dict] = []

    for f in filters:
        groups = f.split(",")
        d = {}
        for g in groups:
            (key, value) = g.split(":")
            d[key] = value
        parsed.append(d)
    return parsed


def _path_for_id(id: str, flat=False):
    if flat:
        return Path(id)
    return Path(id[3:7]) / id


def download_dataset(dl: BakrepDownloader, id: str, filters: List[dict], download_dir: Path, max_retries=3):
    _try = 0
    while _try <= max_retries:
        try:
            dl.download(id, filters, str(download_dir))
            break
        except DownloadFailedException as e:
            if _try == max_retries:
                raise e
            _try += 1


def download(args):
    output_path = Path(args.directory)
    if not output_path.exists():
        output_path.mkdir(parents=True)

    entries = []
    if not args.entries is None:
        entries.extend(_parse_entries(args.entries))

    if not args.tsv is None:
        entries.extend(_parse_ids_from_tsv(args.tsv))

    filters = []
    if not args.filters is None:
        filters = _parse_filters(args.filters)

    set = DownloadSet.at_location(
        args.directory, ids=entries, skipDownloaded=args.restart, skipToDownload=True)
    dl = BakrepDownloader()
    log = ConsoleOutput(set)
    log.print_progress()
    for id in set.download_list():
        download_dir = output_path / _path_for_id(id, args.flat)

        if not download_dir.exists():
            download_dir.mkdir(parents=True)

        log.print_message(f"Downloading: {id}")
        try:
            download_dataset(dl, id, filters, download_dir)
            set.finish_dataset(id)
            log.print_message(f"Finished: {id}")
        except DownloadFailedException as e:
            log.print_error_message(f"Download failed: {id} {e}")
            log.print_message(f"Download failed: {id}")
            set.failed_dataset(id)
    set.close()


class ConsoleOutput:
    messages: List[str] = []
    error_messages: List[str] = []
    lastlines = 1
    max_messages = 1
    max_error_messages = 5
    first_print = True

    def __init__(self, download_set: DownloadSet):
        self.download_set = download_set

    def print_message(self, msg: str):
        self.messages.append(msg)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        self.print_progress()

    def print_error_message(self, msg: str):
        self.error_messages.append(msg)
        if len(self.error_messages) > self.max_error_messages:
            self.error_messages = self.error_messages[-self.max_error_messages:]
        self.print_progress()

    def print_progress(self):
        ds = self.download_set
        if not self.first_print:
            print(f"\033[{self.lastlines}F", end="", flush=True)
            print(f"\033[2K", end="", flush=True)
        self.first_print = False
        print(
            f"Progress: {ds.downloaded_datasets()}/{ds.total_datasets()}, Failed: {ds.failed_datasets()}")
        for m in self.messages:
            print(f"\033[2K", end="", flush=True)
            print(m)

        print(f"\033[2K", end="", flush=True)
        print("\nLatest Errors:")
        for m in self.error_messages:
            print(f"\033[2K", end="", flush=True)
            print(m)
        self.lastlines = 1 + len(self.messages) + 2 + len(self.error_messages)
