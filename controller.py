import customtkinter as ctk
from view import WeatherAppView
from model import WeatherAppModel


class WeatherAppController:
    def __init__(self, *, city=None, country=None, lat=None, long=None, unit='metric'):
        self.view = WeatherAppView()
        self.model = WeatherAppModel(city, country, lat, long, unit)
        self.view.mainloop()
