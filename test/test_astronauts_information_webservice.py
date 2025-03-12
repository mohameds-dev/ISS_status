import unittest
from unittest.mock import patch
from src.astronauts_information_webservice import *

class TestISSWebService(unittest.TestCase):
    def test_get_response(self):
        self.assertEqual(get_response().keys(), {"people", "number", "message"})

    def test_parse_response_returns_astronauts_names_for_iss_from_sample_data(self):
            sample_data = {
                "message": "success",
                "number": 3,
                "people": [
                    {"name": "Chris Cassidy", "craft": "ISS"},
                    {"name": "Anatoly Ivanishin", "craft": "ISS"},
                    {"name": "Ivan Vagner", "craft": "ISS"}
                ]
            }
            expected_names = ["Chris Cassidy", "Anatoly Ivanishin", "Ivan Vagner"] 

            self.assertEqual(parse_response(sample_data), expected_names)
        
    def test_parse_response_returns_astronauts_names_for_iss_from_another_sample_data(self):
        sample_data = {
            "message": "success",
            "number": 5,
            "people": [
                {"name": "Oleg Novitskiy", "craft": "ISS"},
                {"name": "Nick Hague", "craft": "ISS"},
                {"name": "Vladimir Ivanov", "craft": "Tiangong"}, 
                {"name": "Kate Rubins", "craft": "ISS"}
                
            ]
        }
        expected_names = ["Oleg Novitskiy", "Nick Hague", "Kate Rubins"]

        self.assertEqual(parse_response(sample_data), expected_names)

    @patch("src.astronauts_information_webservice.parse_response")
    @patch("src.astronauts_information_webservice.get_response")
    def test_get_astronauts_names_calls_both(self, mock_get_response, mock_parse):
        dummy_response = {"people": [{"name": "Mock Astronaut", "craft": "ISS"}]}
        mock_get_response.return_value = dummy_response
        mock_parse.return_value = ["Mock Astronaut"]

        result = get_astronauts_names()

        self.assertEqual(result, ["Mock Astronaut"])
        mock_get_response.assert_called_once()
        mock_parse.assert_called_once_with(dummy_response)
    
    @patch("src.astronauts_information_webservice.get_response")
    def test_get_astronauts_names_raises_exception_if_get_response_fails(self, mock_get_response):
        mock_get_response.side_effect = Exception("Get Response error")

        with self.assertRaisesRegex(Exception, "Get Response error"):
            get_astronauts_names()
    
    @patch("src.astronauts_information_webservice.parse_response")
    @patch("src.astronauts_information_webservice.get_response")
    def test_get_astronauts_names_raises_exception_if_parse_response_fails(self, mock_get_response, mock_parse):
        mock_get_response.return_value = {"people": [{"name": "Astronaut", "craft": "ISS"}]}
        mock_parse.side_effect = Exception("Parse Response error")
        
        with self.assertRaisesRegex(Exception, "Parse Response error"):
            get_astronauts_names()
