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
                         font=(FONT, 20)
                         )


class WeatherAnimationCanvas(ctk.CTkCanvas):
    def __init__(self, parent, image_path, fg_color):
        super().__init__(master=parent,
                         bg=fg_color)
        # self.false = None
        # self.last_dem = None
        self.resize_after_id = None  # To keep track of the scheduled resize operation
        self.animate_id = None


        self.image_path = image_path
        self.bind('<Configure>', self.schedule_resize)
        # self.after(500, self.animate)

    def import_images(self):
        # self.img_list = [
        #     Image.open(f"{path}\\{file}").resize((100, 100))
        #     for path, _, files in os.walk(self.image_path)
        #     for file in files
        # ]
        self.img_list = [
            ImageTk.PhotoImage(Image.open(f"{path}\\{file}").resize(self.image_size))
            for path, _, files in os.walk(self.image_path)
            for file in files
        ]
        self.iterable_img = cycle(self.img_list)
        if self.animate_id is not None:
            self.after_cancel(self.animate_id)
        self.animate()

    def get_canvas_dimensions(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height
        image_size = min(self.canvas_width, self.canvas_height)
        self.image_size = (image_size, image_size)
        print(self.image_size)

        self.center_x = event.width // 2
        self.center_y = event.height // 2
        # if self.false is None or self.canvas_width // 80 != self.last_dem:
        self.import_images()
        self.last_dem = self.canvas_width // 80
        print('Imported images')
            # self.false = False
        self.update_idletasks()

    def schedule_resize(self, event):
        # Cancel any previously scheduled resize operation
        if self.resize_after_id is not None:
            self.after_cancel(self.resize_after_id)

        # Schedule a new resize operation to run after 200 milliseconds of inactivity
        self.resize_after_id = self.after(200, lambda: self.get_canvas_dimensions(event))

    def animate(self):
        next_frame = next(self.iterable_img)
        # self.img_tk = ImageTk.PhotoImage(next_frame)
        self.delete('all')
        self.create_image(self.center_x, self.center_y, anchor='center', image=next_frame)
        self.update_idletasks()
        self.animate_id = self.after(50, self.animate)
