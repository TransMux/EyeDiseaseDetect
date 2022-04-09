import unittest
from pathlib import Path

from EyeDiseaseDetect.utils import search_assets_structure


class Test_utils(unittest.TestCase):
    def test_search_assets_structure(self):
        self.assertEqual(search_assets_structure(Path("../data/assets")),
                         [{'children': None, 'label': '1.jpg', 'value': '0>0'},
                          {'children': [{'children': None, 'label': '2.jpg', 'value': '1>0'}],
                           'label': '3月17日',
                           'value': '0>1'}])


if __name__ == '__main__':
    unittest.main()
