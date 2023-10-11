import tempfile
import unittest
from pathlib import Path

from requests_mock import Mocker

from bakrep.cli import main


def mock_result(id: str, suffix: str, attributes: dict,
                md5="d41d8cd98f00b204e9800998ecf8427e"  # md5 sum for no content
                ):
    return {
        "url": f"https://bakrep-data.s3.computational.bio.uni-giessen.de/{id}/{id}.{suffix}",
        "attributes": attributes,
        "md5": md5,
        "size": 0,
    }


def mock_dataset(m: Mocker, id: str):
    dataset = {"id": id, "results": [
        mock_result(id, "fas", {"tool": "test", "filetype": "fas"}),
        mock_result(id, "gff3", {"tool": "test", "filetype": "gff3"}),
        mock_result(id, "json", {"tool": "test", "filetype": "json"})
    ]}
    m.get(
        f"https://bakrep.computational.bio/api/v1/datasets/{id}", json=dataset)
    for r in dataset["results"]:
        m.get(r['url'], text='')


class DownloadCommandTest(unittest.TestCase):
    def test_should_fail_without_tsv_and_without_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit) as cm:
                main(["download", "-d", tmp])

    def test_should_fail_when_download_directory_is_a_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "download"
            f.touch()
            with self.assertRaises(SystemExit) as cm:
                main(["download", "-e", "abc", "-d", str(f)])

    def test_should_create_a_non_existent_download_directory(self):
        with Mocker() as m:
            mock_dataset(m, "abc")
            with tempfile.TemporaryDirectory() as tmp:
                f = Path(tmp) / "download"
                main(["download", "-e", "abc", "-d", str(f), "--flat"])
                self.assertTrue(f.exists())

    def test_should_merge_entries_and_tsv_entries(self):
        with Mocker() as m:
            mock_dataset(m, "abc")
            mock_dataset(m, "xyz")
            mock_dataset(m, "jjj")
            with tempfile.TemporaryDirectory() as tmp:
                tsv_data = "xyz\njjj"
                tsv_path = Path(tmp) / "tsv"
                tsv_path.write_text(tsv_data)
                main(["download", "-e", "abc", "-t", str(tsv_path), "-d", tmp])
                for e in ["xyz", "jjj", "abc"]:
                    self.assertTrue((Path(tmp)/e).is_dir())

    def test_should_download_files(self):
        with Mocker() as m:
            mock_dataset(m, "abc")
            with tempfile.TemporaryDirectory() as tmp:
                main(["download", "-e", "abc", "-d", tmp])
                files = list((Path(tmp) / "abc").iterdir())
                self.assertListEqual(
                    sorted(map(lambda x: x.name, files)),
                    sorted(["abc.fas", "abc.json", "abc.gff3"]))

    def test_should_filter_results(self):
        with Mocker() as m:
            mock_dataset(m, "abc")
            with tempfile.TemporaryDirectory() as tmp:
                main(["download", "-e", "abc", "-d", tmp, "-m", "filetype:gff3"])
                files = list((Path(tmp) / "abc").iterdir())
                self.assertListEqual(
                    sorted(map(lambda x: x.name, files)),
                    sorted(["abc.gff3"]))
