import requests
from collections import namedtuple
from datetime import datetime
from settings import BASE_URL, API_KEY

WeatherData = namedtuple('WeatherData', field_names=('date', 'temp', 'weather_condition', 'feels_like'))
ForecastData = namedtuple('ForecastData', field_names=('today', 'next_5_days'))
LocationData = namedtuple('LocationData', field_names=('country_name', 'city_name', 'latitude', 'longitude'))

def _process_weather_data(data: dict, today=None):
    date = datetime.fromisoformat(data['dt_txt'].split(' ')[0])
    temp = data['main']['temp_max']
    weather_condition = data['weather'][0]['main']
    if today:
        feels_like = data['main']['feels_like']
    else:
        feels_like = None

    return WeatherData(date, temp, weather_condition, feels_like)


def get_weather_data(latitude, longitude, unit):
    url = f'{BASE_URL}&lat={latitude}&lon={longitude}&appid={API_KEY}&units={unit}'

    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()

        today = json_data['list'][0]['dt_txt'].split(' ')[0]
        current_forcast = _process_weather_data(json_data['list'][0], today=True)
        # print(f'{today=}')
        # print(f'{current_forcast=}')
        next_5_days_forecast = [
            _process_weather_data(item)
            for item in json_data['list']
            if '12:00:00' in item['dt_txt'] and today not in item['dt_txt']
        ]
    else:
        raise Exception('Failed to get the weather data')
    return ForecastData(current_forcast, next_5_days_forecast)


def _get_geo_info(city_name):
    # Construct the URL for the API request
    url = f'https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1&accept-language=en'

    # Make the GET request to the API
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON content of the response
        data = response.json()

        # Extract the coordinates
        if data:
            # print(data)
            location = data[0]
            latitude = location['lat']
            longitude = location['lon']
            name = location['display_name'].split(', ')
            country_name = name[-1]
            city_name = name[0]

            # Return the coordinates
            return LocationData(country_name, city_name, latitude, longitude)
        else:
            # print(f"No results found for {city_name}")
            raise Exception(f"No results found for {city_name}")

    else:
        # Print an error message if the request was not successful
        # print(f"Error: Unable to fetch coordinates (status code: {response.status_code})")
        raise Exception(f"Error: Unable to fetch coordinates (status code: {response.status_code})")

    # Example usage
# CITY_NAME = 'birjand'
#
# coordinates = get_coordinates(CITY_NAME)
# if coordinates:
#     latitude, longitude = coordinates
#     print(f"Coordinates of {CITY_NAME}:")
#     print(f"Latitude: {latitude}")
#     print(f"Longitude: {longitude}")
