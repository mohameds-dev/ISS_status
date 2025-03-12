import requests

def get_response():
    return requests.get("http://api.open-notify.org/iss-now.json").json()

def parse_response(data):
    return {"timestamp": data.get("timestamp"), "location": {"latitude": data.get("iss_position").get("latitude"), "longitude": data.get("iss_position").get("longitude")}}
