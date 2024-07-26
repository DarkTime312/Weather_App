import os
from datetime import datetime

from PIL import Image

from settings import WEATHER_DATA
from utils import _get_geo_info, get_weather_data, LocationData, ForecastData, WeatherData

# Define type aliases
type OptionalString = str | None
type OptionalFloat = float | None


class WeatherAppModel:
    def __init__(self,
                 city: OptionalString,
                 country: OptionalString,
                 lat: OptionalFloat,
                 long: OptionalFloat,
                 unit: OptionalString) -> None:

        self.city: OptionalString = city
        self.country: OptionalString = country
        self.latitude: OptionalFloat = lat
        self.longitude: OptionalFloat = long
        self.unit: OptionalString = unit

        self.forecast_img_list = None
        self.animation_img_list = None
        self.current_condition = None
        self.today_date = None
        self.next_days_data = None
        self.feels_like = None
        self.current_temp = None
        self.current_forecast = None
        self.next_5_day_forecast = None

        self.update_geo_info()
        self.get_weather_info()
        self.process_today_data()
        self.process_next_5_days_data()
        self.import_images()

    def update_geo_info(self) -> None:
        """
        Update the geographical information of the object.

        This function updates the object's city, country, latitude, and longitude
        attributes based on the provided information or by fetching data using external APIs.
        """

        def fetch_geo_info() -> LocationData | None:
            """
            Fetch geographical information based on the provided attributes or IP address.

            :return: LocationData named tuple containing city, country, latitude, and longitude.
            :raises Exception: If insufficient information is provided.
            """
            if all(user_provided_info):
                return None  # All necessary information is already provided.
            elif not any(user_provided_info):
                return _get_geo_info()  # Fetch based on IP address.
            elif self.city:
                return _get_geo_info(self.city)  # Fetch based on city name.
            elif self.latitude is not None and self.longitude is not None:
                return _get_geo_info(latitude=self.latitude, longitude=self.longitude)  # Fetch based on coordinates.
            else:
                raise Exception('Provide either no information to use IP location, '
                                'or at least city name or the coordinates.')

        type OptionalString = str | None
        type OptionalFloat = float | None

        # Gather the information provided by user (if any).
        user_provided_info: tuple[OptionalString, OptionalString, OptionalFloat, OptionalFloat] = (
            self.city, self.country, self.longitude, self.latitude
        )

        # Fetch geographical information if necessary
        city_info: LocationData = fetch_geo_info()

        # Update the object's attributes with the fetched information
        if city_info:
            self.city: str = city_info.city_name
            self.country: str = city_info.country_name
            self.latitude: float = city_info.latitude
            self.longitude: float = city_info.longitude

        # Uncomment the following line if you need to debug the updated information
        # print(self.city, self.country, self.latitude, self.longitude)

    def get_weather_info(self) -> None:
        """
        Get the weather information for today and the next few days
        and store the information as attributes.

        :return: None
        """
        data: ForecastData = get_weather_data(latitude=self.latitude,
                                              longitude=self.longitude,
                                              unit=self.unit)
        self.current_forecast: WeatherData = data.today
        self.next_5_day_forecast: list[WeatherData] = data.next_5_days
        # Uncomment for debug
        # print(self.current_forecast, self.next_5_day_forecast)

    @staticmethod
    def get_ordinal_suffix(day_of_month: int) -> str:
        """
        Get the ordinal suffix for a given day of the month.

        :param day_of_month: The day of the month.
        :return: The ordinal suffix ('st', 'nd', 'rd', 'th') for the given day.
        """
        if 11 <= day_of_month <= 13:
            return 'th'
        else:
            return {1: 'st', 2: 'nd', 3: 'rd'}.get(day_of_month % 10, 'th')

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """
        Format a datetime object into a readable format.

        The returned string is in the format: 'DayOfWeek, DayOrdinalSuffix MonthName'
        Example: 'Mon, 1st January'


        :param dt: The datetime object to format.

        :return: The formatted date string.
        """
        # Get the day number and its ordinal suffix
        day: int = dt.day
        suffix: str = WeatherAppModel.get_ordinal_suffix(day)
        # Format the date string
        formatted_date: str = dt.strftime(f'%a, {day}{suffix} %B')
        return formatted_date

    def process_today_data(self) -> None:
        """
        Process and format today's weather data for display.

        This method updates the instance attributes with formatted weather data
        for the current day, including the date, current temperature, feels-like
        temperature, and weather condition. The temperature values are rounded
        and appended with the degree symbol (°).

        :return: None
        """
        self.today_date: str = self.format_datetime(self.current_forecast.date)
        self.current_temp: str = f'{round(self.current_forecast.temp)}\N{DEGREE SIGN}'
        self.feels_like: str = f'{round(self.current_forecast.feels_like)}\N{DEGREE SIGN}'
        self.current_condition: str = self.current_forecast.weather_condition
        # Uncomment for debug
        # print(self.today_date, self.current_temp, self.feels_like)

    def process_next_5_days_data(self) -> None:
        """
        Process and format the weather data for the next 5 days.

        This method updates the instance attribute `self.next_days_data` with a list of tuples,
        each containing the day of the week, the temperature (rounded and appended with the
        degree symbol), and the weather condition for each of the next 5 days.

        Updates:
            self.next_days_data (list of tuples): Each tuple contains:
                - str: Day of the week (e.g., 'Monday')
                - str: Temperature with degree symbol (e.g., '23°')
                - str: Weather condition description (e.g., 'Clear')
        """

        self.next_days_data = [
            (day_weather_data.date.strftime('%A'), f'{round(day_weather_data.temp)}\N{DEGREE SIGN}', day_weather_data.weather_condition)
            for day_weather_data in self.next_5_day_forecast
        ]
        # Uncomment for debug
        # print(self.next_days_data)

    def import_images(self) -> None:
        """
        Import and process images for weather animations and forecasts.

        This method updates the instance attributes `self.animation_img_list` and
        `self.forecast_img_list` with lists of `PIL.Image` objects. The images are
        loaded from specified directories based on the current weather condition
        and the forecast for the next days.

        """

        # Get the path to the folder which contains the animation pictures
        animation_img_folder: str = WEATHER_DATA[self.current_condition]['path']
        # Create a list of `PIL.Image` files which will be uses to generate an animation.
        self.animation_img_list: list[Image] = [
            Image.open(f"{path}\\{file}")
            for path, _, files in os.walk(animation_img_folder)
            for file in files
        ]
        # Create a list of `PIL.Image` files representing the forecast image for each day.
        self.forecast_img_list: list[Image] = [
            Image.open(f"images\\{condition}.png")
            for _, _, condition in self.next_days_data
        ]
