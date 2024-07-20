from utils import _get_geo_info, get_weather_data, LocationData
from PIL import Image
import os
from settings import WEATHER_DATA


class WeatherAppModel:
    def __init__(self, city, country, lat, long, unit):
        self.city = city
        self.country = country
        self.latitude = lat
        self.longitude = long
        self.unit = unit
        self.forecast_img = None
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
        self.process_next_5_days()
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
            elif self.latitude and self.longitude:
                return _get_geo_info(latitude=self.latitude, longitude=self.longitude)  # Fetch based on coordinates.
            else:
                raise Exception('Provide either no information to use IP location, '
                                'or at least city name or the coordinates.')

        # Check if the user has provided any location information
        user_provided_info = (self.city, self.country, self.longitude, self.latitude)

        # Fetch geographical information if necessary
        city_info = fetch_geo_info()

        # Update the object's attributes with the fetched information
        if city_info:
            self.city = city_info.city_name
            self.country = city_info.country_name
            self.latitude = city_info.latitude
            self.longitude = city_info.longitude

        # Uncomment the following line if you need to debug the updated information
        # print(self.city, self.country, self.latitude, self.longitude)

    def get_weather_info(self):
        data = get_weather_data(latitude=self.latitude,
                                longitude=self.longitude,
                                unit=self.unit)
        self.current_forecast = data.today
        self.next_5_day_forecast = data.next_5_days
        print(self.current_forecast, self.next_5_day_forecast)

    def process_today_data(self):
        self.today_date = self.format_datetime(self.current_forecast.date)
        self.current_temp: str = f'{round(self.current_forecast.temp)}\N{DEGREE SIGN}'
        self.feels_like: str = f'{round(self.current_forecast.feels_like)}\N{DEGREE SIGN}'
        self.current_condition = self.current_forecast.weather_condition
        print(self.today_date, self.current_temp, self.feels_like)

    @staticmethod
    def get_ordinal_suffix(day):
        if 11 <= day <= 13:
            return 'th'
        else:
            return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    def format_datetime(self, dt):
        # Get the day and its ordinal suffix
        day = dt.day
        suffix = self.get_ordinal_suffix(day)
        # Format the date string
        formatted_date = dt.strftime(f'%a, {day}{suffix} %B')
        return formatted_date

    def process_next_5_days(self):
        self.next_days_data = [
            (x.date.strftime('%A'), f'{round(x.temp)}\N{DEGREE SIGN}', x.weather_condition)
            for x in self.next_5_day_forecast
        ]
        print(self.next_days_data)

    def import_images(self):
        animation_path = WEATHER_DATA[self.current_condition]['path']
        self.animation_img_list = [
            Image.open(f"{path}\\{file}")
            for path, _, files in os.walk(animation_path)
            for file in files
        ]
        self.forecast_img = [
            Image.open(f"images\\{condition}.png")
            for _, _, condition in self.next_days_data
        ]
