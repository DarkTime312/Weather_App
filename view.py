try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

import customtkinter as ctk
from settings import *
from components import TodayTemp, LocationLabel, TodayDateLabel, WeatherAnimationCanvas
from PIL import Image, ImageTk


class WeatherAppView(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Window setup
        self.geometry('550x250')
        self.minsize(550, 250)
        self.title('')
        self.configure(padx=5, pady=5)
        self.iconbitmap('images/empty.ico')
        self.set_layout()

    def set_layout(self):
        self.rowconfigure(0, weight=4, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')

        self.columnconfigure((0, 1), weight=1, uniform='b')

    def change_titlebar_color(self, weather_condition) -> None:
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = WEATHER_DATA[weather_condition]['title']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def create_today_temp(self, current_temp, feels_temp, text_color):
        TodayTemp(self, current_temp, feels_temp, text_color).grid(row=0, column=0)

    def create_location_label(self, city, country, text_color):
        LocationLabel(self, city=city, country=country, text_color=text_color).grid(row=1, column=0, sticky='sw')

    def create_date_label(self, text, text_color):
        TodayDateLabel(self, text_color=text_color, text=text).grid(row=1, column=1, sticky='se')

    def create_weather_animation_canvas(self, animation_list, fg_color):
        WeatherAnimationCanvas(self, animation_list, fg_color).grid(row=0, column=1, sticky='news')
