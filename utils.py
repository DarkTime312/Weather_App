from typing import NamedTuple
from datetime import datetime

import requests
import customtkinter

from settings import BASE_URL, API_KEY


class WeatherData(NamedTuple):
    """
    Contains the weather data
    """
    date: datetime
    temp: float
    weather_condition: str
    feels_like: float


class LocationData(NamedTuple):
    """
    A named tuple representing geographical location information.
    """
    country_name: str
    city_name: str
    latitude: float
    longitude: float


class ForecastData(NamedTuple):
    """
    Contains Weather data for today and the next 5 days.
    """
    today: WeatherData
    next_5_days: list[WeatherData]


def get_weather_data(latitude: float, longitude: float, unit: str = 'metric') -> ForecastData:
    """
    Get the weather data for today and the next 5 days for a specified location.

    This function queries an external API to obtain the weather data of a certain coordinate.

    :param latitude: Latitude of desired location as a float number
    :param longitude: Longitude of desired location as a float number
    :param unit: Optional; a string specifying the unit of temperature,
         Defaults to 'metric'.
    :return: A ForecastData object containing the today and the next few days data as separate objects.
    :raises Exception: If the API request fails or returns a non-200 status code.

    """
    url: str = f'{BASE_URL}&lat={latitude}&lon={longitude}&appid={API_KEY}&units={unit}'

    response: requests.Response = requests.get(url)
    if response.status_code == 200:
        json_data: dict = response.json()

        # Find the today's date and get its weather data.
        today_date: str = json_data['list'][0]['dt_txt'].split(' ')[0]
        current_forcast: WeatherData = _process_weather_data(json_data['list'][0], is_today=True)

        # Get the date and weather data of the next 4 or 5 days
        # It will skip the today info
        next_5_days_forecast: list[WeatherData] = [
            _process_weather_data(item)
            for item in json_data['list']
            if '12:00:00' in item['dt_txt'] and today_date not in item['dt_txt']
        ]
    else:
        raise Exception('Failed to get the weather data')
    return ForecastData(current_forcast, next_5_days_forecast)


def _process_weather_data(data: dict, is_today: bool | None = None) -> WeatherData:
    """
    Processes weather data for a specific day and returns it as a WeatherData object.

    This helper function extracts the date, maximum temperature, weather condition,
    and 'feels like' temperature from a given dictionary containing weather data.
    If the data is for today, it includes the 'feels like' temperature; otherwise,
    'feels like' temperature is set to None.

    :param data: A dictionary containing weather data for a specific day.
    :param is_today: A boolean indicating if the data is for today.
    :return: date, max temperature, weather condition and the feels like temperature of the day.
    """
    date: datetime = datetime.fromisoformat(data['dt_txt'].split(' ')[0])
    temp: float = data['main']['temp_max']
    weather_condition: str = data['weather'][0]['main']
    feels_like: float | None = data['main']['feels_like'] if is_today else None

    return WeatherData(date, temp, weather_condition, feels_like)


def _get_geo_info(city_name: str | None = None,
                  latitude: float | None = None,
                  longitude: float | None = None) -> LocationData:
    """
    Get the location information for a specified city, coordinates, or current IP address.

    This function queries external APIs to retrieve geographical information.
    If a city name is specified, it uses the Nominatim API to get the location
    details. If latitude and longitude are provided, it uses the Nominatim API
    to perform reverse geocoding. If no city name or coordinates are provided,
    it uses the IPAPI service to get the location details based on the current IP address.


    :param city_name: Optional; the name of the city for which to retrieve location information.
         If not provided, the function will use the current IP address to determine the location.

    :param latitude: Optional; the latitude coordinate for reverse geocoding.

    :param longitude: Optional; the longitude coordinate for reverse geocoding.

    :return: A named tuple containing country name, city name,
        latitude and longitude.

    :raises Exception: if it can't connect to the API or couldn't
     find the city.
    """

    def _fetch_data(url_: str) -> dict | list:
        """
        A helper function in charge of handling API requests.

        :param url_: API url
        :return: Parsed object
        :raises Exception: if it can't connect to the API.
        """
        response: requests.Response = requests.get(url_, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            raise Exception(f"Error: Unable to fetch data (status code: {response.status_code})")
        return response.json()

    if latitude and latitude:
        url: str = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=10&addressdetails=1&accept-language=en"
        data: dict = _fetch_data(url)
        address: dict = data.get('address', {})
        city: str = address.get('city', address.get('town', address.get('village', '')))
        country: str = address.get('country', '')
        return LocationData(country, city, latitude, longitude)

    if city_name:
        url = f'https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1&accept-language=en'
    else:
        url = "https://ipapi.co/json/"
    data: dict | list = _fetch_data(url)
    if not data:
        raise Exception(f"No results found for {city_name}")

    if city_name:
        location: dict = data[0]
        latitude: float = float(location['lat'])
        longitude: float = float(location['lon'])
        location_full_name: list[str] = location['display_name'].split(', ')
        country_name: str = location_full_name[-1]
        city_name: str = location_full_name[0]
    else:
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        country_name: str = data['country_name']
        city_name: str = data['city']

    return LocationData(country_name, city_name, latitude, longitude)


def reset_grid_layout(container: customtkinter.CTk) -> None:
    """
    Reset the grid layout of a given container in a customtkinter application.

    This function removes all widgets from the grid layout of the specified
    container and resets the row and column configurations to their default
    state (weight=0, uniform='').

    Args:
        container (customtkinter.CTk): The container whose grid layout is to be reset.
    """

    # Remove all widgets from the grid
    for widget in container.winfo_children():
        widget.grid_forget()

    # Reset row and column configurations
    for i in range(container.grid_size()[1]):  # Number of rows
        container.grid_rowconfigure(i, weight=0, uniform='')

    for j in range(container.grid_size()[0]):  # Number of columns
        container.grid_columnconfigure(j, weight=0, uniform='')
