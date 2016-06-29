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
        result = get_json_from_gtop("ligands/x/")
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {"name": "superdrug", "ligandId": 1})


    @patch("requests.get")
    def test_can_process_json_with_strange_response(self, mock_get):
        self.mock_response.text = ""
        mock_get.return_value = self.mock_response
        result = get_json_from_gtop("ligands/1/")
        self.assertIs(result, None)
        self.mock_response.text = "A non-JSON sentence"
        result = get_json_from_gtop("ligands/x/")
        self.assertIs(result, None)


    @patch("requests.get")
    def test_can_process_json_500_error(self, mock_get):
        self.mock_response.status_code = 500
        mock_get.return_value = self.mock_response
        result = get_json_from_gtop("ligands/x/")
        self.assertIs(result, None)



class RetryTests(TestCase):

    def setUp(self):
        self.mock_response = unittest.mock.Mock()
        self.mock_response.text = ""
        self.mock_response.status_code = 500


    @patch("requests.get")
    def test_json_retriever_will_try_five_times(self, mock_get):
        mock_get.return_value = self.mock_response
        result = get_json_from_gtop("ligands/x/")
        self.assertEqual(mock_get.call_count, 5)


    @patch("requests.get")
    def test_json_retriever_attempt_number_can_be_varied(self, mock_get):
        mock_get.return_value = self.mock_response
        result = get_json_from_gtop("ligands/x/", attempts=3)
        self.assertEqual(mock_get.call_count, 3)
        result = get_json_from_gtop("ligands/x/", attempts=1)
        self.assertEqual(mock_get.call_count, 1 + 3)
        result = get_json_from_gtop("ligands/x/", attempts=9)
        self.assertEqual(mock_get.call_count, 9 + 1 + 3)


    @patch("requests.get")
    def test_attempts_must_be_int(self, mock_get):
        mock_get.return_value = self.mock_response
        with self.assertRaises(TypeError):
            get_json_from_gtop("ligands/x/", attempts=1.5)
        with self.assertRaises(TypeError):
            get_json_from_gtop("ligands/x/", attempts="x")


    @patch("requests.get")
    def test_attempts_must_be_positive(self, mock_get):
        mock_get.return_value = self.mock_response
        with self.assertRaises(ValueError):
            get_json_from_gtop("ligands/x/", attempts=-1)
        with self.assertRaises(ValueError):
            get_json_from_gtop("ligands/x/", attempts=0)


    @patch("requests.get")
    def test_can_get_correct_value_on_last_attempt(self, mock_get):
        ok_response = unittest.mock.Mock()
        ok_response.status_code = 200
        ok_response.text = '{"name": "superdrug", "ligandId": 1}'
        mock_get.side_effect = [
         self.mock_response, self.mock_response, self.mock_response, ok_response
        ]
        self.assertEqual(
         get_json_from_gtop("/ligands/x/"),
         {"name": "superdrug", "ligandId": 1}
        )
        self.assertEqual(mock_get.call_count, 4)
