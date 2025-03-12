from datetime import datetime, timezone, timedelta
from .craft_information_webservice import get_response, parse_response
from .reverse_geocoding import reverse_geocode
import requests

def timestamp_to_ct(timestamp):
    utc_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    ct_timezone = timezone(timedelta(hours=-6))

    return utc_dt.astimezone(ct_timezone).strftime("%I:%M%p")

def iss_location_provider():
    parsed = parse_response(get_response())  
    ct_time = timestamp_to_ct(parsed.get("timestamp"))
    location = reverse_geocode(
        parsed.get("location").get("latitude"),
        parsed.get("location").get("longitude"),
        )
    
    return (ct_time, location)

def get_location(iss_location_provider=iss_location_provider):
    try:
        return iss_location_provider()
    except Exception as e:
        if 'Get' in str(e) or 'Parse' in str(e):
            raise e
        return str(e)        
    
def key_for_sort(name):
    names = name.split()

    return (names[-1], names[0], *names[1:-1],)
    
def get_astronauts(astronauts_detail_provider):
    try:
        return(sorted(astronauts_detail_provider(),  key=key_for_sort))
    except Exception as e:
        return str(e)
