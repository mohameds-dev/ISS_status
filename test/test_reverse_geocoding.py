import unittest
from src.reverse_geocoding import reverse_geocode, parse_city_and_state_code
from unittest.mock import patch
import requests

class TestGetLocationName(unittest.TestCase):
    def test_parse_city_and_state_code_takes_sample_address_and_returns_city_and_state_code(self):
        address = {'suburb': 'Downtown', 'city': 'Baltimore', 'state': 'Maryland', 'ISO3166-2-lvl4': 'US-MD', 'country': 'United States', 'country_code': 'us'}

        self.assertEqual(parse_city_and_state_code(address), "Baltimore, MD")

    def test_parse_city_and_state_code_takes_another_sample_address_and_returns_city_and_state_code(self):
        address = {'village': 'Buranda', 'county': 'Maregaon', 'state_district': 'Yavatmal District', 'state': 'Maharashtra', 'ISO3166-2-lvl4': 'IN-MH', 'country': 'India', 'country_code': 'in'}

        self.assertEqual(parse_city_and_state_code(address), "Buranda, MH")

    @patch("src.reverse_geocoding.requests.get")
    def test_reverse_geocode_takes_latitude_and_longitude_and_returns_location(self, mock_request_get):
        mock_request_get.return_value.json.return_value = {'place_id': 229707033, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright', 'osm_type': 'node', 'osm_id': 9920558966, 'lat': '20.0936092', 'lon': '78.7297332', 'class': 'place', 'type': 'village', 'place_rank': 19, 'importance': 0.14670416800183103, 'addresstype': 'village', 'name': 'Buranda', 'display_name': 'Buranda, Maregaon, Yavatmal District, Maharashtra, India', 'address': {'village': 'Buranda', 'county': 'Maregaon', 'state_district': 'Yavatmal District', 'state': 'Maharashtra', 'ISO3166-2-lvl4': 'IN-MH', 'country': 'India', 'country_code': 'in'}, 'boundingbox': ['20.0736092', '20.1136092', '78.7097332', '78.7497332']}

        self.assertEqual(reverse_geocode(20.093262, 78.717181), "Buranda, MH")

    @patch("src.reverse_geocoding.requests.get")
    def test_reverse_geocode_takes_another_latitude_and_longitude_and_returns_location(self, mock_request_get):
        mock_request_get.return_value.json.return_value = {'place_id': 325730236, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright', 'osm_type': 'relation', 'osm_id': 12792276, 'lat': '39.2911657', 'lon': '-76.6140149', 'class': 'boundary', 'type': 'administrative', 'place_rank': 20, 'importance': 0.3881511276833865, 'addresstype': 'suburb', 'name': 'Downtown', 'display_name': 'Downtown, Baltimore, Maryland, United States', 'address': {'suburb': 'Downtown', 'city': 'Baltimore', 'state': 'Maryland', 'ISO3166-2-lvl4': 'US-MD', 'country': 'United States', 'country_code': 'us'}, 'boundingbox': ['39.2874623', '39.2951379', '-76.6238831', '-76.6047309']}

        self.assertEqual(reverse_geocode(39.289196, -76.609511), "Baltimore, MD")

    @patch("src.reverse_geocoding.requests.get")
    def test_reverse_geocode_takes_another_latitude_and_longitude_and_returns_location(self, mock_request_get):
        mock_request_get.return_value.json.return_value = {'error': 'Unable to geocode'}

        self.assertEqual(reverse_geocode(-58.995813, 17.616077), "Unrecognized location")

    @patch("src.reverse_geocoding.requests.get")
    def test_reverse_geocode_takes_another_latitude_and_longitude_and_returns_location(self, mock_request_get):
        mock_request_get.side_effect = requests.exceptions.RequestException("Network error")
        
        self.assertEqual(reverse_geocode(-58.995813, 17.616077), "Error: Unable to fetch location")
        

    def test_valid_coordinates(self):
        lat, lon = 39.279275, -76.610885
        result = reverse_geocode(lat, lon)

        self.assertEqual("Baltimore, MD", result)

    def test_invalid_coordinates(self):
        lat = 1000.0
        lon = 2000.0
        result = reverse_geocode(lat, lon)
        
        self.assertEqual(result, "Unrecognized location")

    

if __name__ == "__main__":
    unittest.main()