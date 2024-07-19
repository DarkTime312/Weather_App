try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

import customtkinter as ctk
from settings import *
from components import reset_grid, TodayTemp, DateLocationLabel, WeatherAnimationCanvas, NextWeekForecast


class WeatherAppView(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Window setup
        self.geometry('550x250')
        self.minsize(550, 250)
        self.title('')
        self.configure(padx=10, pady=10)
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
                    reset_grid(self)
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
                    self.horizontal_on_right()

    def normal_layout(self):
        reset_grid(self)

        self.rowconfigure(0, weight=4, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')

        self.columnconfigure((0, 1), weight=1, uniform='b')

        self.today_temp.set_layout('normal')
        self.date_location_label.set_layout('normal')
        self.weather_animation_canvas.set_layout('normal')

    def vertical_on_bottom_layout(self):
        reset_grid(self)

        self.rowconfigure(0, weight=3, uniform='a')
        self.rowconfigure(1, weight=4, uniform='a')
        self.rowconfigure(2, weight=3, uniform='a')
        self.rowconfigure(3, weight=3, uniform='a')
        self.columnconfigure(0, weight=1, uniform='b')

        self.date_location_label.set_layout('bottom_vertical')
        self.weather_animation_canvas.set_layout('bottom_vertical')
        self.today_temp.set_layout('bottom_vertical')
        self.next_week_forecast.set_layout('bottom_vertical')
        # ctk.CTkLabel(self, fg_color='red').grid(row=3, column=0, sticky='news')

    def horizontal_on_right(self):
        reset_grid(self)
        self.date_location_label.set_layout('horizontal on the right')
        self.weather_animation_canvas.set_layout('horizontal on the right')
        self.next_week_forecast.set_layout('horizontal on the right')
        self.today_temp.set_layout('horizontal on the right')

        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
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
        self.today_temp = TodayTemp(self, current_temp, feels_temp, text_color)

    def create_date_location_frame(self, city, country, date, text_color):
        self.date_location_label = DateLocationLabel(self, city=city, country=country, text_color=text_color, date=date)

    def create_weather_animation_canvas(self, animation_list, fg_color):
        self.weather_animation_canvas = WeatherAnimationCanvas(self, animation_list, fg_color)

    def create_forecast_object(self, forecast_data, forecast_img_list, seperator_color):
        self.next_week_forecast = NextWeekForecast(self, forecast_data, forecast_img_list, seperator_color)
