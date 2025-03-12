from .iss_information import get_location, get_astronauts
from .astronauts_information_webservice import get_astronauts_names

def main():

    try:
        location_details = get_location()  
        astronauts = get_astronauts(get_astronauts_names)

        print(f"ISS location as {location_details[0]} CT flying over {location_details[1]}")
        print("")
        print(f"There are {len(astronauts)} people on ISS at this time:")
        for name in astronauts:
            print(name)
    except Exception as e:
        print("Service unavailable. Please try again later.")
        print(f"Error: {str(e)}")
        

if __name__ == "__main__":
    main()