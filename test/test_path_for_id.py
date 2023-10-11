import unittest
from pathlib import Path

from bakrep.download import _path_for_id


class PathForIdTest(unittest.TestCase):

    def test_should_have_subpath(self):
        self.assertEqual(_path_for_id("SAMEA3231284"),
                         Path("EA32/SAMEA3231284"))
