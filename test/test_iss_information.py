import unittest
from unittest.mock import patch, MagicMock
from src.iss_information import *
from src.astronauts_information_webservice import *
from src.craft_information_webservice import get_response as get_response_craft_info
from src.craft_information_webservice import parse_response as parse_response_craft_info


class TestGetLocation(unittest.TestCase):
    def test_canary(self):
        self.assertTrue(True)
    
    def test_get_location_returns_time_and_location_that_the_service_returns(self):
        iss_location_service = lambda: ("05:17AM", "Houston, TX")

        self.assertEqual(get_location(iss_location_service), ("05:17AM", "Houston, TX"))

    def throw(self, message):
      raise Exception(message)
    
    def test_get_location_returns_network_error_if_exception(self):
        iss_location_service = lambda: self.throw("network error: service unreachable")
        
        self.assertEqual(get_location(iss_location_service), "network error: service unreachable")
    
    def test_get_location_returns_service_failed_if_timeout(self):
        iss_location_service = lambda: self.throw("service failed to respond")

        self.assertEqual(get_location(iss_location_service), "service failed to respond")

    @patch("src.iss_information.requests.get")
    @patch("src.iss_information.parse_response")
    @patch("src.iss_information.get_response")
    def test_get_location_calls_get_response_and_parse_response(self, mock_get_response, mock_parse_response, _):
        iss_location_provider = lambda: mock_parse_response(mock_get_response()) 
        
        get_location(iss_location_provider)
        
        mock_get_response.assert_called_once()
        mock_parse_response.assert_called_once()

    def test_timestamp_to_ct_with_sample_timestamp(self):
        self.assertEqual(timestamp_to_ct(1741406510), "10:01PM")

    def test_timestamp_to_ct_with_another_sample_timestamp(self):
        self.assertEqual(timestamp_to_ct(1741406682), "10:04PM")

    @patch("src.iss_information.get_response")
    def test_get_location_returns_the_time_in_CT_instead_of_timestamp(self, mock_get_response):
        mock_get_response.return_value = {"timestamp": 1741406682, "iss_position": {"latitude": "48.6150", "longitude": "-23.9530"}}

        return_value = get_location(iss_location_provider)
    
        self.assertIn("10:04PM", return_value)

    @patch("src.iss_information.get_response")
    def test_get_location_returns_the_place_of_iss(self, mock_get_response):
        mock_get_response.return_value = {"timestamp": 1741406682, "iss_position": {"latitude": "39.289196", "longitude": "-76.609511"}}
        return_value = get_location(iss_location_provider)
    
        self.assertIn("Baltimore, MD", return_value)

    @patch("src.iss_information.get_response")
    def test_get_location_raises_exception_if_get_response_throws_an_exception(self, mock_get_response):
        mock_get_response.side_effect = Exception("Get Response error")
        iss_location_provider = lambda: parse_response(mock_get_response())

        with self.assertRaisesRegex(Exception, "Get Response error"):
            get_location(iss_location_provider)

    @patch("src.iss_information.parse_response")
    @patch("src.iss_information.get_response")
    def test_get_location_raises_exception_if_parse_response_throws_an_exception(self, mock_get_response, mock_parse_response):
        mock_get_response.return_value = {"dummy": "data"}
        mock_parse_response.side_effect = Exception("Parse Response error")
        iss_location_provider = lambda: mock_parse_response(mock_get_response())

        with self.assertRaisesRegex(Exception, "Parse Response error"):
            get_location(iss_location_provider)


    def test_get_astronauts_returns_empty_list(self):
        astronauts_detail_provider = lambda: []

        self.assertEqual(get_astronauts(astronauts_detail_provider), [])

    def test_get_astronauts_returns_one_name(self):
        astronauts_detail_provider = lambda: ["Nikolai Chub"]

        self.assertEqual(get_astronauts(astronauts_detail_provider), ["Nikolai Chub"])

    def test_get_astronauts_returns_two_names_sorted(self):
        astronauts_detail_provider = lambda: ["Nikolai Chub", "Matthew Dominick"]

        self.assertEqual(get_astronauts(astronauts_detail_provider), ["Nikolai Chub", "Matthew Dominick"])

    def test_get_astronauts_returns_two_names_unsorted(self):
        astronauts_detail_provider = lambda: ["Matthew Dominick","Nikolai Chub"] 

        self.assertEqual(get_astronauts(astronauts_detail_provider), ["Nikolai Chub", "Matthew Dominick"])  

    def test_get_astronauts_returns_two_names_same_last_names_and_unsorted_first_names(self):
        astronauts_detail_provider = lambda: ["Robert Martin", "Alice Martin"] 

        self.assertEqual(get_astronauts(astronauts_detail_provider), ["Alice Martin", "Robert Martin"])  

    def test_get_astronauts_returns_network_error_if_exception(self):
        astronauts_detail_provider = lambda: self.throw("network error: service unreachable")
        
        self.assertEqual(get_astronauts(astronauts_detail_provider), "network error: service unreachable")
    
    def test_get_astronauts_returns_service_failed_if_timeout(self):
        astronauts_detail_provider = lambda: self.throw("service failed to respond")

        self.assertEqual(get_astronauts(astronauts_detail_provider), "service failed to respond") 

    def test_get_astronauts_returns_two_names_same_last_names_and_different_middle_and_first_names(self):
        astronauts_detail_provider = lambda: ["Robert C Martin", "Alice B Martin"]

        self.assertEqual(get_astronauts(astronauts_detail_provider), ["Alice B Martin", "Robert C Martin"])  

    def test_get_astronauts_returns_two_names_same_last_names_and_first_names_and_different_middle_names(self):
        astronauts_detail_provider = lambda: ["Robert C Martin", "Robert B Martin"]

        self.assertEqual(get_astronauts(astronauts_detail_provider), ["Robert B Martin", "Robert C Martin"])  
