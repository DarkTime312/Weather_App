from view import WeatherAppView
from model import WeatherAppModel
from settings import *


class WeatherAppController:
    def __init__(self, *, city=None, country=None, lat=None, long=None, unit='metric'):
        self.model = WeatherAppModel(city, country, lat, long, unit)
        self.view = WeatherAppView()
        self.config_colors()
        self.create_widgets()
        self.view.mainloop()

    def config_colors(self) -> None:
        """
        Change the color of title bar and window background.

        This function will get the current weather condition from model
        And based on that will change the app colors.

        :return: None
        """
        color: dict = WEATHER_DATA[self.model.current_condition]
        self.view.change_titlebar_color(color['title'])
        self.view.configure(fg_color=color['main'])

    def create_widgets(self):
        self.view.create_today_temp(self.model.current_temp,
                                    self.model.feels_like,
                                    WEATHER_DATA[self.model.current_condition]['text']
                                    )
        self.view.create_date_location_frame(city=self.model.city,
                                             country=self.model.country,
                                             text_color=WEATHER_DATA[self.model.current_condition]['text'],
                                             date=self.model.today_date)
        self.view.create_weather_animation_canvas(self.model.animation_img_list,
                                                  WEATHER_DATA[self.model.current_condition]['main'])
        self.view.create_forecast_object(forecast_data=self.model.next_days_data,
                                         forecast_img_list=self.model.forecast_img_list,
                                         seperator_color=WEATHER_DATA[self.model.current_condition]['divider color'])
