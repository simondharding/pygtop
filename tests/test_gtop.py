from unittest import TestCase
import unittest.mock
from unittest.mock import patch
from pygtop.gtop import get_json_from_gtop

class JsonTests(TestCase):

    def setUp(self):
        self.mock_response = unittest.mock.Mock()
        self.mock_response.text = '{"name": "superdrug", "ligandId": 1}'
        self.mock_response.status_code = 200


    @patch("requests.get")
    def test_can_process_json(self, mock_get):
        mock_get.return_value = self.mock_response
        result = get_json_from_gtop("ligands/1/")
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {"name": "superdrug", "ligandId": 1})


    @patch("requests.get")
    def test_can_process_json_with_strange_response(self, mock_get):
        self.mock_response.text = ""
        mock_get.return_value = self.mock_response
        result = get_json_from_gtop("ligands/1/")
        self.assertIs(result, None)
        self.mock_response.text = "A non-JSON sentence"
        result = get_json_from_gtop("ligands/1/")
        self.assertIs(result, None)


    @patch("requests.get")
    def test_can_process_json_500_error(self, mock_get):
        self.mock_response.status_code = 500
        mock_get.return_value = self.mock_response
        result = get_json_from_gtop("ligands/1/")
        self.assertIs(result, None)




'''import unittest
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
    unittest.main()'''
