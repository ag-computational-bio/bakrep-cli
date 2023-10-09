import unittest
from bakrep.model import BakrepDownloader, DownloadFailedException
import tempfile
from pathlib import Path
import requests_mock


def mockdataset(m, id):
    m.get(f"https://bakrep.computational.bio/api/v1/datasets/{id}",
          content=Path(f"./test/data/scenarios/download-dataset/{id}.json").read_bytes())


def mockdownload(m, id, file):
    m.get(f"https://bakrep-data.s3.computational.bio.uni-giessen.de/{id}/{id}.{file}",
          content=Path(f"./test/data/scenarios/download-dataset/{id}.{file}").read_bytes())


def mockserver(m, id):
    mockdataset(m, id)
    mockdownload(m, id, "bakta.json.gz")
    mockdownload(m, id, "bakta.faa.gz")
    mockdownload(m, id, "bakta.ffn.gz")
    mockdownload(m, id, "bakta.gbff.gz")
    mockdownload(m, id, "bakta.gff3.gz")
    mockdownload(m, id, "mlst.json.gz")
    mockdownload(m, id, "assemblyscan.json.gz")
    mockdownload(m, id, "gtdbtk.json.gz")
    mockdownload(m, id, "checkm2.json.gz")


class BakrepDownloaderTest(unittest.TestCase):

    def test_download_without_filter_should_save_everything_in_the_provided_directory(self):
        with requests_mock.Mocker() as m:
            id = "SAMEA3231284"
            mockserver(m, id)

            with tempfile.TemporaryDirectory() as tmp:
                d = BakrepDownloader()
                d.download(id, [], tmp)
                p = Path(tmp)
                files = set(list(map(lambda x: x.name, p.iterdir())))
                expected = set([
                    f"{id}.bakta.json.gz",
                    f"{id}.bakta.ffn.gz",
                    f"{id}.bakta.faa.gz",
                    f"{id}.bakta.gbff.gz",
                    f"{id}.bakta.gff3.gz",
                    f"{id}.assemblyscan.json.gz",
                    f"{id}.checkm2.json.gz",
                    f"{id}.gtdbtk.json.gz",
                    f"{id}.mlst.json.gz",
                ])
                self.assertEqual(files, expected)

    def test_download_with_filter_should_only_save_requested_files_in_the_provided_directory(self):
        with requests_mock.Mocker() as m:
            id = "SAMEA3231284"
            mockserver(m, id)

            with tempfile.TemporaryDirectory() as tmp:
                d = BakrepDownloader()
                d.download(id, [{"tool": "mlst"}, {"tool": "gtdbtk"}], tmp)
                p = Path(tmp)
                files = set(list(map(lambda x: x.name, p.iterdir())))
                expected = set([
                    f"{id}.mlst.json.gz",
                    f"{id}.gtdbtk.json.gz",
                ])
                self.assertEqual(files, expected)

    def test_download_dataset_fails_should_raise_exception(self):
        with requests_mock.Mocker() as m:
            id = "SAMEA3231284"
            m.get(
                f"https://bakrep.computational.bio/api/v1/datasets/{id}", status_code=404)
            with tempfile.TemporaryDirectory() as tmp:
                d = BakrepDownloader()
                self.assertRaises(DownloadFailedException, lambda: d.download(
                    id, [{"tool": "mlst"}, {"tool": "gtdbtk"}], tmp))

    def test_download_result_fails_should_raise_exception(self):
        with requests_mock.Mocker() as m:
            id = "SAMEA3231284"
            mockdataset(m, id)
            m.get(
                f"https://bakrep-data.s3.computational.bio.uni-giessen.de/{id}/{id}.gtdbtk.json.gz", status_code=404)
            with tempfile.TemporaryDirectory() as tmp:
                d = BakrepDownloader()
                self.assertRaises(DownloadFailedException, lambda: d.download(
                    id, [{"tool": "gtdbtk"}], tmp))
