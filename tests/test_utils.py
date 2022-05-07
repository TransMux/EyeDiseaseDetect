import unittest
from pathlib import Path

from EyeDiseaseDetect.utils import search_assets_structure


class Test_utils(unittest.TestCase):
    def test_search_assets_structure(self):
        self.assertEqual(search_assets_structure(Path("../data/assets"), Path("../data/assets")),
                         [{'label': '1.png', 'value': '1.png', 'children': None,
                           'meta': {'create_time': 1649496336, 'result': []}}, {'label': '3月17日', 'value': '3月17日',
                                                                                'children': [
                                                                                    {'label': '2.png',
                                                                                     'value': '3月17日\\2.png',
                                                                                     'children': None,
                                                                                     'meta': {
                                                                                         'create_time': 1649496336,
                                                                                         'result': []}}],
                                                                                'meta': None}]

                         )


if __name__ == '__main__':
    unittest.main()
