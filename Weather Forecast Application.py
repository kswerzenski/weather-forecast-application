# DSC510
# Final Project
# Intro to Programming
# Author Kristen Swerzenski
# 8/12/23

# Importing the requests module
import requests


# Function to look up lat and long from geocoding API using city and state
def city_lookup(city, state):
    base_url = 'https://api.openweathermap.org/geo/1.0/direct'
    api_key = 'f52374474f95baf89a9aaab6f7ece28d'

    try:
        # Building query string for API request
        city_state = f"{city},{state},US"
        params = {'q': city_state, 'limit': 1, 'appid': api_key}

        # Sending 'get' request to API
        # Raising an error if status code is a problem
        location_response = requests.get(base_url, params=params)
        location_response.raise_for_status()

        # Parsing the JSON response data to get latitude and longitude
        location_data = location_response.json()
        if location_data and isinstance(location_data, list):
            latitude = location_data[0]['lat']
            longitude = location_data[0]['lon']
            return latitude, longitude
        # Handling error if invalid city/state is input
        else:
            print(f"Location data for {city}, {state} not available.")
            return None

    # Handling connection errors when calling to API and displaying error
    except requests.exceptions.RequestException as e:
        print("Connection error occurred:", e)
        return None


# Function to look up lat and long from geocoding API using zip code
def zip_lookup(zip_code):
    base_url = 'https://api.openweathermap.org/geo/1.0/zip'
    api_key = 'f52374474f95baf89a9aaab6f7ece28d'

    try:
        # Building query string for API request
        params = {'zip': zip_code, 'appid': api_key}

        # Sending 'get' request to API
        # Raising an error if status code is a problem
        location_response = requests.get(base_url, params=params)
        location_response.raise_for_status()

        # Parsing the JSON response data to get latitude and longitude
        location_data = location_response.json()
        if location_data and isinstance(location_data, dict):
            latitude = location_data['lat']
            longitude = location_data['lon']
            return latitude, longitude
        # Handling error if zip code does not retrieve lat and long
        else:
            print("Location data not available.")
            return None

    # Handling invalid zip code inputs and connection errors with API
    except requests.exceptions.RequestException as e:
        if e.response is not None and e.response.status_code == 404:
            print("Invalid Zip Code")
        else:
            print("Connection error occurred:", e)
        return None


# Function to get weather data using coordinates and units
def get_weather(lat, lon, units):
    api_key = 'f52374474f95baf89a9aaab6f7ece28d'
    base_url = 'https://api.openweathermap.org/data/2.5/weather'

    try:
        # Building query string for API request
        params = {'lat': lat, 'lon': lon, 'appid': api_key, 'units': units}

        # Sending 'get' request to API
        # Raising an error if status code is a problem
        response_weather = requests.get(base_url, params=params)
        response_weather.raise_for_status()

        # Returning the response JSON containing weather data
        return response_weather.json()

    # Handling connection errors and displaying error message
    except requests.exceptions.RequestException as e:
        print("Connection error occurred:", e)
        return None


# Function to display formatted weather information to user
def display_weather(weather_data, units):
    # Handling if no weather data was retrieved
    if weather_data is None:
        print("Weather data not available.")
        return

    # Extracting necessary weather information from the JSON response
    city_name = weather_data['name']
    main_condition = weather_data['weather'][0]['main']
    weather_desc = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    temp_high = weather_data['main']['temp_max']
    temp_low = weather_data['main']['temp_min']
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']

    # Determining appropriate unit symbol based on user's unit preference
    if units == 'metric':
        unit_symbol = '°C'
    elif units == 'imperial':
        unit_symbol = '°F'
    else:
        unit_symbol = 'K'

    # Creating a list of tuples to store weather information from JSON retrieval
    weather_list = [
            ("City:", city_name),
            ("Main Conditions:", main_condition),
            ("Description:", weather_desc),
            ("Temperature:", f"{temp:.1f} {unit_symbol}"),
            ("Feels like:", f"{feels_like:.1f} {unit_symbol}"),
            ("High Temperature:", f"{temp_high:.1f} {unit_symbol}"),
            ("Low Temperature:", f"{temp_low:.1f} {unit_symbol}"),
            ("Pressure:", f"{pressure:.1f} hPa"),
            ("Humidity:", f"{humidity}%")
        ]

    # Calculating the maximum key length to align the output format
    max_key_length = max(len(key) for key, _ in weather_list)

    # Generating the formatted output string by iterating through weather_list
    output = "\n".join(f"{key:{max_key_length}}  {value}" for key, value
                       in weather_list)

    # Displaying formatted weather information
    print(f"Today's Weather for {city_name}:")
    print('-' * 40)
    print(output)
    print('-' * 40)


# Defining main function
def main():
    # Displaying welcome message to user and giving them weather lookup options
    print("Welcome to Clear Skies Weather!")

    # Starting loop to loop program until user exits
    while True:
        print("\nSelect an option:")
        print("1. Lookup Weather by Zip Code")
        print("2. Lookup Weather by City Name")
        print("0. Exit")

        # Prompting user for their choice of preferred lookup method
        choice = input("Enter your choice: ")

        if choice == '1':
            # If user chooses 1,enter zip code and pass into zip_lookup function
            zip_code = input("Enter zip code: ")
            location_info = zip_lookup(zip_code)

            if location_info is not None:
                # If location successfully retrieved, get lat/long
                latitude, longitude = location_info
                # Prompt user for preferred units and convert for API call
                units = input(
                    "Enter preferred units (C, F, or K): ").lower()
                if units == 'c':
                    units = 'metric'
                elif units == 'f':
                    units = 'imperial'
                elif units == 'k':
                    units = 'standard'
                else:
                    print(
                        "Invalid units input. Using default (°F) units.")
                    units = 'imperial'

                # Retrieving and displaying weather data
                weather_data = get_weather(latitude, longitude, units)
                display_weather(weather_data, units)

        elif choice == '2':
            # If user chooses 2,enter city/state and pass into city_lookup
            city_name = input("Enter city name: ")
            state = input("Enter state (ex. New Jersey): ")
            location_info = city_lookup(city_name, state)

            if location_info is not None:
                # If location successfully retrieved, get lat/long
                latitude, longitude = location_info
                # Prompt user for preferred units and convert for API call
                units = input(
                    "Enter preferred units (C, F, or K): ").lower()
                if units == 'c':
                    units = 'metric'
                elif units == 'f':
                    units = 'imperial'
                elif units == 'k':
                    units = 'standard'
                else:
                    print(
                        "Invalid units input. Using default (°F) units.")
                    units = 'imperial'

                # Retrieving and displaying weather data
                weather_data = get_weather(latitude, longitude, units)
                display_weather(weather_data, units)

        elif choice == '0':
            # If user enters 0, exit program and display goodbye message
            print("Thank you for using Clear Skies Weather. Goodbye!")
            break

        else:
            # Handling invalid user inputs
            print("Invalid choice. Please try again.")


# Calling main function
if __name__ == "__main__":
    main()
