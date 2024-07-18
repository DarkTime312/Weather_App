try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

import customtkinter as ctk
from settings import *
from components import TodayTemp, DateLocationLabel, WeatherAnimationCanvas
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
        self.bind('<Configure>', self.decide_layout)
        self.current_layout = None

    def decide_layout(self, event):
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        # print(window_width, window_height)

        if window_width < 1000:
            if window_height < 600:
                mode = 'Normal mode'
                if self.current_layout != mode:
                    self.current_layout = mode
                    self.normal_layout()
                    print('Normal mode')
                    # print(window_width, window_height)
            else:
                mode = 'vertical on bottom'
                if self.current_layout != mode:
                    self.current_layout = mode
                    self.reset_grid()
                    print('vertical on bottom')
                    self.vertical_on_bottom_layout()
                    # print(window_width, window_height)

        else:
            if window_height < 600:
                mode = 'vertical on the right side'
                if self.current_layout != mode:
                    self.current_layout = mode
                    print('vertical on the right side')
                    # print(window_width, window_height)

            else:
                mode = 'horizontal on the right'
                if self.current_layout != mode:
                    self.current_layout = mode
                    print('horizontal on the right')
                    # print(window_width, window_height)

    def normal_layout(self):
        self.reset_grid()

        self.rowconfigure(0, weight=4, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')

        self.columnconfigure((0, 1), weight=1, uniform='b')

        self.today_temp.set_layout('normal')
        self.date_location_label.set_layout('normal')
        self.weather_animation_canvas.grid(row=0, column=1, sticky='news')

    def vertical_on_bottom_layout(self):
        self.reset_grid()

        self.rowconfigure(0, weight=3, uniform='a')
        self.rowconfigure(1, weight=5, uniform='a')
        self.rowconfigure(2, weight=3, uniform='a')
        self.rowconfigure(3, weight=5, uniform='a')
        # self.rowconfigure(4, weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='b')

        self.date_location_label.set_layout('bottom_vertical')
        self.weather_animation_canvas.grid(row=1, column=0, sticky='news')
        self.today_temp.set_layout('bottom_vertical')
        ctk.CTkLabel(self, fg_color='red').grid(row=3, column=0, sticky='news')

    def reset_grid(self):
        # Remove all widgets from the grid
        for widget in self.winfo_children():
            widget.grid_forget()

        # Reset row and column configurations
        for i in range(self.grid_size()[1]):  # Number of rows
            self.grid_rowconfigure(i, weight=0, uniform='')
        for j in range(self.grid_size()[0]):  # Number of columns
            self.grid_columnconfigure(j, weight=0, uniform='')

    def change_titlebar_color(self, weather_condition) -> None:
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
