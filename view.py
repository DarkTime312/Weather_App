try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

import customtkinter as ctk
from settings import *
from components import TodayTemp


class WeatherAppView(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Window setup
        self.geometry('550x250')
        self.minsize(550, 250)
        self.title('')
        self.iconbitmap('images/empty.ico')

    def change_titlebar_color(self, weather_condition) -> None:
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = WEATHER_DATA[weather_condition]['title']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def create_today_temp(self, current_temp, feels_temp, text_color):
        TodayTemp(self, current_temp, feels_temp, text_color).pack()
