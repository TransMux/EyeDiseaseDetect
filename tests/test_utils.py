import unittest
from pathlib import Path

from EyeDiseaseDetect.utils import search_assets_structure


class Test_utils(unittest.TestCase):
    def test_search_assets_structure(self):
        self.assertEqual(search_assets_structure(Path("../data/assets")),
                         [{'label': '1.jpg', 'value': '0>0', 'children': None,
                           'meta': {'create_time': 1649496336, 'result': []}}, {'label': '3月17日', 'value': '0>2',
                                                                                'children': [
                                                                                    {'label': '2.jpg', 'value': '1>0',
                                                                                     'children': None,
                                                                                     'meta': {'create_time': 1649496336,
                                                                                              'result': []}}],
                                                                                'meta': None}]
                         )


if __name__ == '__main__':
    unittest.main()
