import urllib.request
import json
import requests
from weather_data import _get_geo_info, get_weather_data
from PIL import Image
import os
from settings import WEATHER_DATA
class WeatherAppModel:
    def __init__(self, city, country, lat, long, unit):
        self.forecast_img = None
        self.animation_img_list = None
        self.current_condition = None
        self.today_date = None
        self.next_days_data = None
        self.feels_like = None
        self.current_temp = None
        self.city = city
        self.country = country
        self.latitude = lat
        self.longitude = long
        self.unit = unit
        self.current_forecast = None
        self.next_5_day_forecast = None
        self.check_data()
        self.get_weather_info()
        self.process_today_data()
        self.process_next_5_days()
        self.import_images()

    def check_data(self):
        # If user did not provide any location, find the location based on ip
        variables = (self.city, self.country, self.longitude, self.latitude)
        # If user provided all the parameters, use them
        if all(variables):
            return
        # If none of the parameters are provided, use the ip
        if not any(variables):
            print('current loc')
            with urllib.request.urlopen("https://ipapi.co/json/") as url:
                data = json.loads(url.read().decode())
                self.city = data['city']
                self.country = data['country_name']
                self.latitude = data['latitude']
                self.longitude = data['longitude']
        # If user at least provided city name
        elif self.city:
            city_info = _get_geo_info(self.city)
            self.city = city_info.city_name
            self.country = city_info.country_name
            self.latitude = city_info.latitude
            self.longitude = city_info.longitude
        else:
            raise Exception('Either pass nothing to use the ip location,'
                            ' or pass city name to get the info from web,'
                            ' or pass all the parameters')
        print(self.city, self.country, self.latitude, self.longitude)

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
