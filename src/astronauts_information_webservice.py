import requests

def get_response():
    return requests.get("http://api.open-notify.org/astros.json").json()

def parse_response(response):
    CRAFT = "ISS"

    return [person["name"] for person in response["people"] if person.get("craft") == CRAFT] 

def get_astronauts_names():
    return parse_response(get_response())
