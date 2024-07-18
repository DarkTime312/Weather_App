import customtkinter as ctk
from settings import *
from PIL import Image, ImageTk
import os
from itertools import cycle


class TodayTemp(ctk.CTkFrame):
    def __init__(self, parent, current_temp, feels_temp, text_color):
        super().__init__(master=parent, fg_color='transparent')
        self.current_temp = current_temp
        self.feels_temp = feels_temp
        self.text_color = text_color

        self.set_layout()
        self.create_widgets()

    def set_layout(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)

    def create_widgets(self):
        self.temp_date = ctk.CTkLabel(self,
                                      text=self.current_temp,
                                      text_color=self.text_color,
                                      font=(FONT, 50))
        self.temp_date.grid(row=0, column=0, sticky='news')

        self.feels_label = ctk.CTkLabel(self,
                                        text=f'feels like: {self.feels_temp}',
                                        text_color=self.text_color,
                                        font=(FONT, 15)
                                        )
        self.feels_label.grid(row=1, column=0, sticky='news')


class LocationLabel(ctk.CTkFrame):
    def __init__(self, parent, city, country, text_color):
        super().__init__(master=parent, fg_color='transparent')
        self.text_color = text_color
        self.city = city
        self.country = country
        self.set_layout()
        self.create_widgets()

    def set_layout(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def create_widgets(self):
        city_label = ctk.CTkLabel(self,
                                  text_color=self.text_color,
                                  text=self.city + ', ',
                                  font=(FONT, 20, 'bold'))
        city_label.grid(row=0, column=0)

        country_label = ctk.CTkLabel(self,
                                     text_color=self.text_color,
                                     text=self.country,
                                     font=(FONT, 18))
        country_label.grid(row=0, column=1)


class TodayDateLabel(ctk.CTkLabel):
    def __init__(self, parent, text_color, text):
        super().__init__(master=parent,
                         text_color=text_color,
                         text=text,
                         font=(FONT, 18)
                         )


class WeatherAnimationCanvas(ctk.CTkCanvas):
    def __init__(self, parent, image_path):
        super().__init__(master=parent,
                         bg='red')
        self.image_path = image_path
        # self.bind('<Configure>', self.get_canvas_dimensions)
        self.import_images()

    def import_images(self):
        # self.img_list = [
        #     Image.open(f"{path}\\{file}").resize((100, 100))
        #     for path, _, files in os.walk(self.image_path)
        #     for file in files
        # ]
        self.img_list = [
            ImageTk.PhotoImage(Image.open(f"{path}\\{file}").resize((150, 150)))
            for path, _, files in os.walk(self.image_path)
            for file in files
        ]
        self.iterable_img = cycle(self.img_list)
        self.animate()

    # def get_canvas_dimensions(self, event):
    #     self.import_images()

    def animate(self):
        next_frame = next(self.iterable_img)
        # self.img_tk = ImageTk.PhotoImage(next_frame)
        self.delete('all')
        self.create_image(0, 0, anchor='nw', image=next_frame)
        self.update()
        self.after(50, self.animate)
