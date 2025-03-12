import unittest
from src.craft_information_webservice import *
from parameterized import parameterized

class TestCraftWebService(unittest.TestCase):
    def test_get_response(self):
        response = get_response()

        self.assertEqual(response.keys(), {"message", "iss_position", "timestamp"})
        self.assertEqual(response.get("iss_position").keys(), {"latitude", "longitude"})


    def test_parse_response(self):
        data = {
            "timestamp": 1741264293,
            "iss_position": {"latitude": "-51.4346", "longitude": "6.6050"},
            "message": "success"
        }
        expected_value = {
            "timestamp": 1741264293,
            "location": {"latitude": "-51.4346", "longitude": "6.6050"}
        }
        self.assertEqual(parse_response(data), expected_value)

    def test_parse_response_returns_timestamp_and_location_from_another_sample_data(self):
        data = {
            "timestamp": 1609459200,
            "iss_position": {"latitude": "12.3456", "longitude": "65.4321"},
            "message": "success"
        }
        expected_value = {
            "timestamp": 1609459200,
            "location": {"latitude": "12.3456", "longitude": "65.4321"}
        }
        self.assertEqual(parse_response(data), expected_value)
