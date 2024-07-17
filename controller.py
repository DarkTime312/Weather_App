import customtkinter as ctk
from view import WeatherAppView
from model import WeatherAppModel


class WeatherAppController:
    def __init__(self, *, city=None, country=None, lat=None, long=None):
        self.view = WeatherAppView()
        self.model = WeatherAppModel(city, country, lat, long)
        self.view.mainloop()
