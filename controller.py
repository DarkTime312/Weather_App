import customtkinter as ctk
from view import WeatherAppView
from model import WeatherAppModel
from settings import *


class WeatherAppController:
    def __init__(self, *, city=None, country=None, lat=None, long=None, unit='metric'):
        self.view = WeatherAppView()
        self.model = WeatherAppModel(city, country, lat, long, unit)
        self.config_colors()
        self.small_layout()
        self.view.mainloop()

    def config_colors(self):
        self.view.change_titlebar_color(self.model.current_condition)
        self.view.configure(fg_color=WEATHER_DATA[self.model.current_condition]['main'])

    def small_layout(self):
        self.view.create_today_temp(self.model.current_temp,
                                    self.model.feels_like,
                                    WEATHER_DATA[self.model.current_condition]['text']
                                    )
        self.view.create_location_label(city=self.model.city,
                                        country=self.model.country,
                                        text_color=WEATHER_DATA[self.model.current_condition]['text'])
        self.view.create_date_label(text=self.model.today_date,
                                    text_color=WEATHER_DATA[self.model.current_condition]['text'])
        self.view.create_weather_animation_canvas(WEATHER_DATA[self.model.current_condition]['path'])
