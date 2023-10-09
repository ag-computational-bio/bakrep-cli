from typing import Collection, List
from pathlib import Path


class Result:
    def __init__(self, url: str, attributes: dict, md5: str, size: int):
        self.url = url
        self.attributes = attributes
        self.md5 = md5
        self.size = size

    def __eq__(self, other):
        if isinstance(other, Result):
            return self.url == other.url and self.attributes == other.attributes
        return False

    def __str__(self):
        return f"Result[ {self.url}, {self.attributes}, {self.md5}, {self.size}]"

    def matches(self, filters: List[dict]):
        for f in filters:
            matches = True
            for pair in f.items():
                if self.attributes[pair[0]] != pair[1]:
                    matches = False
                    break
            if matches:
                return True
        return False


class Dataset:
    def __init__(self, id: str, results: List[Result]):
        self.id = id
        self.results = results

    def filter(self, filters: List[dict]):
        if (len(filters) == 0):
            return self.results
        filtered = []
        for r in self.results:
            if r.matches(filters):
                filtered.append(r)
        return filtered


class DownloadSet:
    """
    A collection of datasets that should be downloaded
    """

    def __init__(self, location: Path, toDownload=set(), downloaded=set()):
        self.location = location
        self.toDownload = toDownload
        self.downloaded = downloaded
        self.__downloaded_writer__ = open(location/'downloaded.dat', "a")
        self.__toDownload_writer__ = open(location/'toDownload.dat', "a")

    def close(self):
        self.__downloaded_writer__.close()
        self.__toDownload_writer__.close()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def __enter__(self):
        return self

    def add_dataset(self, datasetId: str):
        first = len(self.toDownload) == 0
        self.toDownload.add(datasetId)
        if not first:
            self.__toDownload_writer__.write("\n")
        self.__toDownload_writer__.write(datasetId)

    def finish_dataset(self, datasetId: str):
        first = len(self.downloaded) == 0
        self.downloaded.add(datasetId)
        self.toDownload.remove(datasetId)
        if not first:
            self.__downloaded_writer__.write("\n")
        self.__downloaded_writer__.write(datasetId)

    @staticmethod
    def at_location(path: str, ids: Collection[str] = set(), skipDownloaded=False, skipToDownload=False):
        """
        Factory for a downloadset that persists the downloaded ids to disc
        """
        p = Path(path) / '.progress'
        toDownloadPath = p / 'toDownload.dat'
        downloadedPath = p / 'downloaded.dat'
        downloaded = set()
        toDownload = set(ids)
        if not p.exists():
            p.mkdir(parents=True)

        if not skipDownloaded and downloadedPath.exists():
            downloaded = set(downloadedPath.read_text().split("\n"))
        else:
            downloadedPath.write_text("\n".join(downloaded))
        if not skipToDownload and toDownloadPath.exists():
            toDownload = set(toDownloadPath.read_text().split("\n"))
        else:
            toDownloadPath.write_text("\n".join(toDownload))
        return DownloadSet(p, toDownload, downloaded)
