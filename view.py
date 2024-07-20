try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

import customtkinter as ctk

from settings import *
from components import TodayTemp, DateLocationLabel, WeatherAnimationCanvas, NextWeekForecast
from utils import reset_grid_layout


class WeatherAppView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.geometry('550x250')
        self.minsize(550, 250)
        self.title('')
        self.configure(padx=10, pady=10)
        self.iconbitmap('images/empty.ico')

        self.bind('<Configure>', self.layout_manager)
        self.layout_functions = {
            'Normal mode': self.normal_layout,
            'vertical on bottom': self.vertical_on_bottom_layout,
            'vertical on the right side': self.vertical_on_right_layout,
            'horizontal on the right': self.horizontal_on_right_layout
        }

        self.active_layout = None

    def layout_manager(self, event) -> None:
        window_width: int = self.winfo_width()
        window_height: int = self.winfo_height()
        # print(window_width, window_height)
        current_mode: str | None = None

        if window_width < 1000 and window_height < 600:
            current_mode: str = 'Normal mode'
        elif window_width < 1000 and window_height >= 600:
            current_mode: str = 'vertical on bottom'
        elif window_width >= 1000 and window_height < 600:
            current_mode: str = 'vertical on the right side'
        elif window_width >= 1000 and window_height >= 600:
            current_mode: str = 'horizontal on the right'

        if self.active_layout != current_mode:
            # print(current_mode)
            self.active_layout: str = current_mode
            self.layout_functions[current_mode]()

    def normal_layout(self):
        reset_grid_layout(self)

        self.rowconfigure(0, weight=6, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')

        self.columnconfigure((0, 1), weight=1, uniform='b')

        self.today_temp.set_layout('normal')
        self.date_location_label.set_layout('normal')
        self.weather_animation_canvas.set_layout('normal')

    def vertical_on_bottom_layout(self):
        reset_grid_layout(self)

        self.rowconfigure(0, weight=18, uniform='a')
        self.rowconfigure(1, weight=28, uniform='a')
        self.rowconfigure(2, weight=24, uniform='a')
        self.rowconfigure(3, weight=30, uniform='a')
        self.columnconfigure(0, weight=1, uniform='b')

        self.date_location_label.set_layout('bottom_vertical')
        self.weather_animation_canvas.set_layout('bottom_vertical')
        self.today_temp.set_layout('bottom_vertical')
        self.next_week_forecast.set_layout('bottom_vertical')
        # ctk.CTkLabel(self, fg_color='red').grid(row=3, column=0, sticky='news')

    def horizontal_on_right_layout(self):
        reset_grid_layout(self)
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.columnconfigure((0, 1), weight=1, uniform='b')

        self.date_location_label.set_layout('horizontal on the right')
        self.weather_animation_canvas.set_layout('horizontal on the right')
        self.next_week_forecast.set_layout('horizontal on the right')
        self.today_temp.set_layout('horizontal on the right')

    def vertical_on_right_layout(self):
        reset_grid_layout(self)

        self.rowconfigure(0, weight=6, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        # self.rowconfigure(tuple(range(3)), weight=1, uniform='a')
        # self.rowconfigure(tuple(range(3)), weight=1, uniform='a')
        # self.rowconfigure(tuple(range(3)), weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=4, uniform='b')

        self.date_location_label.set_layout('vertical on the right')
        self.next_week_forecast.set_layout('vertical on the right')
        self.today_temp.set_layout('vertical on the right')
        self.weather_animation_canvas.set_layout('vertical on the right')

    def change_titlebar_color(self, weather_condition: str) -> None:
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = WEATHER_DATA[weather_condition]['title']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def create_today_temp(self, current_temp, feels_temp, text_color):
        self.today_temp = TodayTemp(self, current_temp, feels_temp, text_color)

    def create_date_location_frame(self, city, country, date, text_color):
        self.date_location_label = DateLocationLabel(self, city=city, country=country, text_color=text_color, date=date)

    def create_weather_animation_canvas(self, animation_list, fg_color):
        self.weather_animation_canvas = WeatherAnimationCanvas(self, animation_list, fg_color)

    def create_forecast_object(self, forecast_data, forecast_img_list, seperator_color):
        self.next_week_forecast = NextWeekForecast(self, forecast_data, forecast_img_list, seperator_color)
