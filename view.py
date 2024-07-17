try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

import customtkinter as ctk
from settings import *


class WeatherAppView(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Window setup
        self.geometry('550x250')
        self.minsize(550, 250)
        self.title('')
        self.iconbitmap('images/empty.ico')
        self.change_titlebar_color()

    def change_titlebar_color(self) -> None:
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = WEATHER_DATA['Clear']['title']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass
