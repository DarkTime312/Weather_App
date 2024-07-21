from itertools import cycle
from typing import Iterable, Generator
import time

import customtkinter as ctk
from PIL import ImageTk

from settings import *
from utils import reset_grid_layout


class TodayTemp(ctk.CTkFrame):
    def __init__(self, parent, current_temp, feels_temp, text_color):
        super().__init__(master=parent, fg_color='transparent')
        self.current_temp = current_temp
        self.feels_temp = feels_temp
        self.text_color = text_color
        self.feels_label = None
        self.temp_date = None

        self.create_widgets()

    def set_layout(self, layout):
        if layout in {'normal', 'vertical on the right'}:
            self.grid(row=0, column=0)
        elif layout == 'bottom_vertical':
            self.grid(row=2, column=0)
        elif layout == 'horizontal on the right':
            self.grid(row=3, column=0, sticky='n')

    def create_widgets(self):
        self.temp_date = ctk.CTkLabel(self,
                                      text=self.current_temp,
                                      text_color=self.text_color,
                                      font=(FONT, TODAY_TEMP_FONT_SIZE))

        self.feels_label = ctk.CTkLabel(self,
                                        text=f'feels like: {self.feels_temp}',
                                        text_color=self.text_color,
                                        font=(FONT, SMALL_FONT_SIZE)
                                        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)

        self.temp_date.grid(row=0, column=0, sticky='news')
        self.feels_label.grid(row=1, column=0, sticky='news')


class DateLocationLabel(ctk.CTkFrame):
    def __init__(self, parent, city, country, text_color, date):
        super().__init__(master=parent, fg_color='transparent')
        self.text_color = text_color
        self.city = city
        self.country = country
        self.date = date

        self.today_date_label = None
        self.country_label = None
        self.city_label = None
        self.address_frame = None

        self.create_widgets()

    def set_layout(self, layout):
        reset_grid_layout(self)

        if layout in {'normal', 'vertical on the right'}:
            self.grid(row=1, column=0, columnspan=2, sticky='sew')

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)

            self.address_frame.grid(row=0, column=0, sticky='news')
            self.today_date_label.grid(row=0, column=1, sticky='e', padx=5)

        elif layout in {'bottom_vertical', 'horizontal on the right'}:
            self.grid(row=0, column=0, sticky='news')

            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)
            self.columnconfigure(0, weight=1)

            self.address_frame.grid(row=0, column=0, sticky='s')
            self.today_date_label.grid(row=1, column=0, sticky='n')

    def create_widgets(self):
        self.address_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.city_label = ctk.CTkLabel(self.address_frame,
                                       text_color=self.text_color,
                                       text=f'{self.city}, ',
                                       font=(FONT, REGULAR_FONT_SIZE, 'bold'))

        self.country_label = ctk.CTkLabel(self.address_frame,
                                          text_color=self.text_color,
                                          text=self.country,
                                          font=(FONT, REGULAR_FONT_SIZE))

        self.city_label.pack(side='left')
        self.country_label.pack(side='left')

        self.today_date_label = ctk.CTkLabel(self,
                                             text_color=self.text_color,
                                             text=self.date,
                                             font=(FONT, REGULAR_FONT_SIZE)
                                             )


class WeatherAnimationCanvas(ctk.CTkCanvas):
    def __init__(self, parent, animation_list, fg_color):
        super().__init__(master=parent,
                         bg=fg_color,
                         bd=0,
                         highlightthickness=0)
        self.animation_list = animation_list

        self.center_x = None
        self.center_y = None
        self.iterable_img = None
        self.last_resize_time = None
        self.is_animating = None
        self.check_scheduled = None

        self.bind('<Configure>', self.schedule_resize)

    def set_layout(self, layout: str):
        if layout in {'normal', 'vertical on the right'}:
            self.grid(row=0, column=1, sticky='news')
        elif layout in {'bottom_vertical', 'horizontal on the right'}:
            self.grid(row=1, column=0, sticky='news')

    def schedule_resize(self, event):
        # Turn off the animation
        self.is_animating = False
        # Remove the last animation frame
        self.delete('all')
        # Store the time that user done the last resize action
        self.last_resize_time = time.time()

        # If the check for resume mechanism isn't active already, activate it
        if not self.check_scheduled:
            self.check_resume()
            self.check_scheduled = True

    def check_resume(self):
        # If at least 300 milliseconds is passed since the last resize action
        # Assume user is done resizing the window, so we can start the animation
        # Otherwise just keep checking
        if time.time() - self.last_resize_time > ANIMATION_PAUSE_TIME:
            self.last_resize_time = None
            self.check_scheduled = False
            self.start_animation()
        else:
            # Check again in 100 milliseconds
            self.after(50, self.check_resume)

    def start_animation(self):
        # Get the new window dimensions
        size = self.get_canvas_dimensions()
        self.iterable_img = self.import_images(size)
        # Start the animation
        self.is_animating = True
        self.animate()

    def get_canvas_dimensions(self) -> tuple[int, int]:
        # Get the dimensions of the new resized
        canvas_width: int = self.winfo_width()
        canvas_height: int = self.winfo_height()
        # Use the lowest of the 2 numbers to decide the width and height
        # of new image which we want to be a square shape
        minimum_size: int = min(canvas_width, canvas_height)

        # Store the coordinates to center of the canvas
        self.center_x: int = canvas_width // 2
        self.center_y: int = canvas_height // 2

        return minimum_size, minimum_size

    def import_images(self, image_size: tuple[int, int]) -> Iterable[ImageTk]:
        # Import the images with new size
        # And create an infinite iterable
        image_generator: Generator = (
            ImageTk.PhotoImage(image.resize(image_size))
            for image in self.animation_list
        )
        return cycle(image_generator)

    def animate(self):
        if self.is_animating:
            next_frame: ImageTk = next(self.iterable_img)
            self.delete('all')
            self.create_image(self.center_x, self.center_y, image=next_frame)
            self.after(ANIMATION_SPEED, self.animate)


class NextWeekForecast(ctk.CTkFrame):
    def __init__(self, parent, forecast_data, forecast_img, seperator_color):
        super().__init__(master=parent, fg_color='white', corner_radius=20)

        self.forecast_data = forecast_data
        self.forecast_img = forecast_img
        self.seperator_color = seperator_color

        self.number_of_needed_row_or_columns = (len(forecast_data) * 2) - 1

    def set_layout(self, layout):
        reset_grid_layout(self)
        if layout == 'bottom_vertical':
            self.grid(row=3, column=0, sticky='news')
            self.rowconfigure(0, weight=1)
            for i in range(self.number_of_needed_row_or_columns):
                uniform = 'a' if i % 2 == 0 else 'b'
                self.columnconfigure(i, weight=1, uniform=uniform)
        if layout == 'horizontal on the right':
            self.grid(row=0, column=1, rowspan=4, sticky='news')
            self.columnconfigure(0, weight=1, uniform='c')

            for i in range(self.number_of_needed_row_or_columns):
                uniform = 'a' if i % 2 == 0 else 'b'
                self.rowconfigure(i, weight=1, uniform=uniform)

        if layout == 'vertical on the right':
            self.grid(row=0, column=2, rowspan=2, sticky='news')
            self.rowconfigure(0, weight=1)

            for i in range(self.number_of_needed_row_or_columns):
                uniform = 'a' if i % 2 == 0 else 'b'
                self.columnconfigure(i, weight=1, uniform=uniform)
        if layout == 'normal':
            pass

        self.create_widgets(layout)

    def create_widgets(self, layout: str):
        data = zip(self.forecast_data, self.forecast_img)

        for widget in self.winfo_children():
            widget.destroy()

        if layout == 'bottom_vertical' or layout == 'vertical on the right':
            for i in range(self.number_of_needed_row_or_columns):
                if i % 2 == 0:
                    (day_text, temp_text, _), img = next(data)
                    frm = ctk.CTkFrame(self, fg_color='transparent')
                    frm.grid(row=0, column=i, sticky='news')
                    ForecastCanvas(frm, img).pack(fill='both')
                    ctk.CTkLabel(frm, text=temp_text, font=(FONT, REGULAR_FONT_SIZE)).pack(expand=True,
                                                                                           fill='x')
                    ctk.CTkLabel(frm, text=day_text[:3], font=(FONT, SMALL_FONT_SIZE)).pack(expand=True,
                                                                                            fill='x')
                else:
                    separator = ctk.CTkFrame(self, fg_color=self.seperator_color, width=3)
                    separator.grid(row=0, column=i, sticky='ns')
        elif layout == 'horizontal on the right':
            for i in range(self.number_of_needed_row_or_columns):
                if i % 2 == 0:
                    (day_text, temp_text, _), img = next(data)
                    frm = ctk.CTkFrame(self, fg_color='transparent')
                    frm.grid(row=i, column=0, sticky='news')
                    ForecastCanvas(frm, img).pack(side='right', fill='both', padx=5)
                    ctk.CTkLabel(frm, text=temp_text, font=(FONT, REGULAR_FONT_SIZE), anchor='e',
                                 fg_color='transparent').pack(
                        side='right', expand=True, fill='both', padx=5)
                    ctk.CTkLabel(frm, text=day_text, font=(FONT, SMALL_FONT_SIZE)).pack(side='left', expand=True,
                                                                                        fill='both')
                else:
                    separator = ctk.CTkFrame(self, fg_color=self.seperator_color, height=3)
                    separator.grid(row=i, column=0, sticky='ew')


class ForecastCanvas(ctk.CTkCanvas):
    def __init__(self, parent, image):
        super().__init__(master=parent, bg='white', bd=0, highlightthickness=0)
        self.image_tk = None
        self.image = image
        self.bind('<Configure>', self.on_configure)

    def on_configure(self, event):
        max_length = min(event.width, event.height)
        if event.width == max_length and event.height == max_length:
            image = self.image.resize((max_length, max_length))
            self.image_tk = ImageTk.PhotoImage(image)
            self.insert_image(max_length // 2)
        else:
            # Set both width and height to the smaller dimension
            self.configure(width=max_length, height=max_length)

    def insert_image(self, center):
        self.delete("all")  # Clear the canvas
        self.create_image(center, center, image=self.image_tk)
