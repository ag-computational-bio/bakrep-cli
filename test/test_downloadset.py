import unittest
from bakrep.model import DownloadSet
import tempfile


class PersistDownloadSetTest(unittest.TestCase):
    ids = ['a', 'b', 'c']

    def test_initial_toDownload_ids_should_be_persisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            with DownloadSet.at_location(tmp, self.ids) as ds:
                pass
            with DownloadSet.at_location(tmp) as ds:
                self.assertEqual(set(self.ids), ds.toDownload)

    def test_toDownload_ids_should_be_persisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            with DownloadSet.at_location(tmp) as ds:
                for id in self.ids:
                    ds.add_dataset(id)
            with DownloadSet.at_location(tmp) as ds:
                self.assertEqual(set(self.ids), ds.toDownload)

    def test_downloaded_ids_should_be_persisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            with DownloadSet.at_location(tmp, self.ids) as ds:
                self.assertEqual(set(self.ids), ds.toDownload)
                ds.finish_dataset("b")
                self.assertEqual(['b'], list(ds.downloaded))
            with DownloadSet.at_location(tmp) as ds:
                self.assertEqual(set(self.ids), ds.toDownload)
                self.assertEqual(['b'], list(ds.downloaded))

    def test_downloaded_should_be_ignored_when_skipDownloaded_is_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            with DownloadSet.at_location(tmp, self.ids) as ds:
                ds.finish_dataset("b")
            with DownloadSet.at_location(tmp, skipDownloaded=True) as ds:
                self.assertEqual(set(), ds.downloaded)

    def test_toDownload_should_be_ignored_when_skipToDownload_is_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            with DownloadSet.at_location(tmp, self.ids) as ds:
                ds.finish_dataset("b")
            with DownloadSet.at_location(tmp, skipToDownload=True) as ds:
                self.assertEqual(set(), ds.toDownload)
