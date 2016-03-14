import unittest
import json
import sys
sys.path.append(".")
from pygtop.gtop import *

class GetJson(unittest.TestCase):

    def test_can_get_json(self):
        json_data = get_json_from_gtop("/ligands/1")
        self.assertIsInstance(json_data, dict)


    def test_invalid_query_returns_none(self):
        json_data = get_json_from_gtop("/ligands/0")
        self.assertEqual(json_data, None)


    def test_gtop_constants_are_valid(self):
        self.assertIsInstance(
         get_json_from_gtop("/ligands/1/%s" % STRUCTURAL_PROPERTIES),
         dict
        )
        self.assertIsInstance(
         get_json_from_gtop("/ligands/1/%s" % MOLECULAR_PROPERTIES),
         dict
        )
        self.assertIsInstance(
         get_json_from_gtop("/ligands/1/%s" % DATABASE_PROPERTIES),
         list
        )
        self.assertIsInstance(
         get_json_from_gtop("/ligands/1/%s" % SYNONYM_PROPERTIES),
         list
        )
        self.assertIsInstance(
         get_json_from_gtop("/ligands/121/%s" % COMMENT_PROPERTIES),
         dict
        )
        self.assertIsInstance(
         get_json_from_gtop("/ligands/4890/%s" % PRECURSOR_PROPERTIES),
         list
        )


if __name__ == "__main__":
    unittest.main()
