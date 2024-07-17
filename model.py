import urllib.request
import json
import requests
from weather_data import _get_geo_info


class WeatherAppModel:
    def __init__(self, city, country, lat, long):
        self.city = city
        self.country = country
        self.latitude = lat
        self.longitude = long
        self.check_data()

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
        pass
