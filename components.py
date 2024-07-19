import customtkinter as ctk
from settings import *
from PIL import Image, ImageTk
from itertools import cycle
import time


def reset_grid(container):
    # Remove all widgets from the grid
    for widget in container.winfo_children():
        widget.grid_forget()

    # Reset row and column configurations
    for i in range(container.grid_size()[1]):  # Number of rows
        container.grid_rowconfigure(i, weight=0, uniform='')
    for j in range(container.grid_size()[0]):  # Number of columns
        container.grid_columnconfigure(j, weight=0, uniform='')


class TodayTemp(ctk.CTkFrame):
    def __init__(self, parent, current_temp, feels_temp, text_color):
        super().__init__(master=parent, fg_color='transparent')
        self.current_temp = current_temp
        self.feels_temp = feels_temp
        self.text_color = text_color

        self.create_widgets()

    def set_layout(self, layout):
        # reset_grid(self)
        if layout == 'normal':
            self.grid(row=0, column=0)

            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=2)
            self.rowconfigure(1, weight=1)

            self.temp_date.grid(row=0, column=0, sticky='news')
            self.feels_label.grid(row=1, column=0, sticky='news')
        elif layout == 'bottom_vertical':
            self.grid(row=2, column=0)
        elif layout == 'horizontal on the right':
            self.grid(row=3, column=0, sticky='n')
        elif layout == 'vertical on the right':
            self.grid(row=0, column=0)

    def create_widgets(self):
        self.temp_date = ctk.CTkLabel(self,
                                      text=self.current_temp,
                                      text_color=self.text_color,
                                      font=(FONT, 50))

        self.feels_label = ctk.CTkLabel(self,
                                        text=f'feels like: {self.feels_temp}',
                                        text_color=self.text_color,
                                        font=(FONT, 15)
                                        )


class DateLocationLabel(ctk.CTkFrame):
    def __init__(self, parent, city, country, text_color, date):
        super().__init__(master=parent, fg_color='transparent')
        self.text_color = text_color
        self.city = city
        self.country = country
        self.date = date
        self.create_widgets()

    def set_layout(self, layout):
        reset_grid(self)

        if layout == 'normal' or layout == 'vertical on the right':
            self.grid(row=1, column=0, columnspan=2, sticky='sew')

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)

            self.address_frame.grid(row=0, column=0, sticky='news')
            self.today_date_label.grid(row=0, column=1, sticky='e', padx=5)

        elif layout == 'bottom_vertical' or layout == 'horizontal on the right':
            self.grid(row=0, column=0, sticky='news')

            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)
            self.columnconfigure(0, weight=1)

            self.address_frame.grid(row=0, column=0, sticky='s')
            self.today_date_label.grid(row=1, column=0, sticky='n', padx=5)

    def create_widgets(self):
        self.address_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.city_label = ctk.CTkLabel(self.address_frame,
                                       text_color=self.text_color,
                                       text=self.city + ', ',
                                       font=(FONT, 20, 'bold'))

        self.country_label = ctk.CTkLabel(self.address_frame,
                                          text_color=self.text_color,
                                          text=self.country,
                                          font=(FONT, 18))

        self.today_date_label = ctk.CTkLabel(self,
                                             text_color=self.text_color,
                                             text=self.date,
                                             font=(FONT, 20)
                                             )
        self.city_label.pack(side='left')
        self.country_label.pack(side='left')


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
        self.animate_id = None
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
        if time.time() - self.last_resize_time > 0.3:
            self.last_resize_time = None
            self.check_scheduled = False
            self.start_animation()
        else:
            self.after(100, self.check_resume)

    def start_animation(self):
        # Get the new window dimensions
        size = self.get_canvas_dimensions()
        self.iterable_img = self.import_images(size)
        # Start the animation
        self.is_animating = True
        self.animate()

    def get_canvas_dimensions(self):
        # Get the dimensions of the new resized
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()
        # Use the lowest of the 2 numbers to decide the width and height
        # of new image which we want to be a square shape
        minimum_size = min(canvas_width, canvas_height)

        # Store the coordinates to center of the canvas
        self.center_x = canvas_width // 2
        self.center_y = canvas_height // 2

        return minimum_size, minimum_size

    def import_images(self, image_size):
        # Import the images with new size
        # And create an infinite iterable
        img_list = [
            ImageTk.PhotoImage(image.resize(image_size))
            for image in self.animation_list
        ]
        return cycle(img_list)

    def animate(self):
        if self.is_animating:
            next_frame = next(self.iterable_img)
            self.delete('all')
            self.create_image(self.center_x, self.center_y, image=next_frame)
            self.animate_id = self.after(50, self.animate)


class NextWeekForecast(ctk.CTkFrame):
    def __init__(self, parent, forecast_data, forecast_img, seperator_color):
        self.forecast_data = forecast_data
        self.forecast_img = forecast_img
        self.seperator_color = seperator_color
        self.num_days = (len(forecast_data) * 2) - 1
        super().__init__(master=parent, fg_color='white', corner_radius=20)

    def set_layout(self, layout):
        reset_grid(self)
        if layout == 'bottom_vertical':
            self.grid(row=3, column=0, sticky='news')
            self.rowconfigure(0, weight=1)
            for i in range(self.num_days):
                uniform = 'a' if i % 2 == 0 else 'b'
                self.columnconfigure(i, weight=1, uniform=uniform)
        if layout == 'horizontal on the right':
            self.grid(row=0, column=1, rowspan=4, sticky='news')
            self.columnconfigure(0, weight=1, uniform='c')

            for i in range(self.num_days):
                uniform = 'a' if i % 2 == 0 else 'b'
                self.rowconfigure(i, weight=1, uniform=uniform)

        if layout == 'vertical on the right':
            self.grid(row=0, column=2, rowspan=2, sticky='news')
            self.rowconfigure(0, weight=1)

            for i in range(self.num_days):
                uniform = 'a' if i % 2 == 0 else 'b'
                self.columnconfigure(i, weight=1, uniform=uniform)

        self.create_widgets(layout)

    def create_widgets(self, layout):
        test = zip(self.forecast_data, self.forecast_img)
        for widget in self.winfo_children():
            widget.destroy()

        if layout == 'bottom_vertical' or layout == 'vertical on the right':
            for i in range(self.num_days):
                if i % 2 == 0:
                    (day_text, temp_text, weather_condition), img = next(test)
                    frm = ctk.CTkFrame(self, fg_color='transparent', corner_radius=20)
                    frm.grid(row=0, column=i, sticky='news')
                    ForecastCanvas(frm, img).pack(side='top', fill='both', anchor='center')
                    ctk.CTkLabel(frm, text=temp_text, font=(FONT, 20)).pack(side='top', expand=True, fill='x')
                    ctk.CTkLabel(frm, text=day_text[:3], font=(FONT, 15)).pack(side='bottom', expand=True, fill='x')
                else:
                    separator = ctk.CTkFrame(self, fg_color=self.seperator_color, width=3)
                    separator.grid(row=0, column=i, sticky='ns')
        elif layout == 'horizontal on the right':
            for i in range(self.num_days):
                if i % 2 == 0:
                    (day_text, temp_text, weather_condition), img = next(test)
                    frm = ctk.CTkFrame(self, fg_color='transparent')
                    frm.grid(row=i, column=0, sticky='news')
                    ForecastCanvas(frm, img).pack(side='right', fill='both', padx=5)
                    ctk.CTkLabel(frm, text=temp_text, font=(FONT, 20), anchor='e', fg_color='transparent').pack(
                        side='right', expand=True, fill='both', padx=5)
                    ctk.CTkLabel(frm, text=day_text, font=(FONT, 15)).pack(side='left', expand=True, fill='both')
                else:
                    separator = ctk.CTkFrame(self, fg_color=self.seperator_color, height=3)
                    separator.grid(row=i, column=0, sticky='ew')


class ForecastCanvas(ctk.CTkCanvas):
    def __init__(self, parent, image):
        super().__init__(master=parent, bg='white', bd=0, highlightthickness=0)
        self.image = image
        self.bind('<Configure>', self.insert_image)

    def insert_image(self, event):
        # Determine the new size, keeping the aspect ratio square
        new_size = min(event.width, event.height)
        self.configure(width=new_size, height=new_size)  # Set both width and height to the smaller dimension

        canvas_width = event.width
        canvas_height = event.height
        # print(f'{event=}')
        img_size = min(canvas_width, canvas_height)
        image = self.image.resize((img_size, img_size))
        self.image_tk = ImageTk.PhotoImage(image)
        self.delete("all")  # Clear the canvas
        self.create_image(canvas_width // 2, canvas_height // 2, anchor='center', image=self.image_tk)
