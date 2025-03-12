import requests

def parse_city_and_state_code(address):
    city = address.get("city") or address.get("town") or address.get("village") or address.get("hamlet")
    state_code = address.get("ISO3166-2-lvl4", "").split('-')[-1]

    return ", ".join(filter(None, (city, state_code)))

def reverse_geocode(latitude, longitude):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json",
        "zoom": 14,
        "addressdetails": 1,
    }
    headers = {
        "User-Agent": "iss_location_app/1.0 (sychandg@cougarnet.uh.edu)",
        "Accept-Language": "en"
    }

    try:
        response = requests.get(url, params=params, headers=headers).json()
        return "Unrecognized location" if 'error' in response.keys() else parse_city_and_state_code(response.get('address'))
    except Exception as e:
        return "Error: Unable to fetch location"
