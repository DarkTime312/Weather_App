import customtkinter as ctk
from settings import *
from PIL import Image, ImageTk
from itertools import cycle


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
        # self.set_layout('normal')

    def set_layout(self, layout):
        reset_grid(self)

        if layout == 'normal':
            self.grid(row=1, column=0, columnspan=2, sticky='sew')

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)

            self.address_frame.grid(row=0, column=0, sticky='news')
            self.today_date_label.grid(row=0, column=1, sticky='e')

        elif layout == 'bottom_vertical' or layout == 'horizontal on the right':
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
                         bg=fg_color)
        # self.false = None
        # self.last_dem = None
        self.resize_after_id = None  # To keep track of the scheduled resize operation
        self.animate_id = None
        self.animation_list = animation_list

        self.bind('<Configure>', self.schedule_resize)
        # self.after(500, self.animate)

    def set_layout(self, layout: str):
        if layout == 'normal':
            self.grid(row=0, column=1, sticky='news')
        elif layout == 'bottom_vertical':
            self.grid(row=1, column=0, sticky='news')
        elif layout == 'horizontal on the right':
            self.grid(row=1, column=0, sticky='news')

    def import_images(self):
        # self.img_list = [
        #     Image.open(f"{path}\\{file}").resize((100, 100))
        #     for path, _, files in os.walk(self.image_path)
        #     for file in files
        # ]
        self.img_list = [
            ImageTk.PhotoImage(image.resize(self.image_size))
            for image in self.animation_list
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
        # print(self.image_size)

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


class NextWeekForecast(ctk.CTkFrame):
    def __init__(self, parent, forecast_data, forecast_img, seperator_color):
        self.forecast_data = forecast_data
        self.forecast_img = forecast_img
        self.seperator_color = seperator_color
        super().__init__(master=parent, fg_color='white', corner_radius=20)

    def set_layout(self, layout):
        reset_grid(self)
        if layout == 'bottom_vertical':
            self.grid(row=3, column=0, sticky='news')
            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1, uniform='a')
            self.columnconfigure(1, weight=1, uniform='b')
            self.columnconfigure(2, weight=1, uniform='a')
            self.columnconfigure(3, weight=1, uniform='b')
            self.columnconfigure(4, weight=1, uniform='a')
            self.columnconfigure(5, weight=1, uniform='b')
            self.columnconfigure(6, weight=1, uniform='a')
        if layout == 'horizontal on the right':
            self.grid(row=0, column=1, rowspan=4, sticky='news')

            self.columnconfigure(0, weight=1, uniform='c')
            self.rowconfigure(0, weight=1, uniform='a')
            self.rowconfigure(1, weight=1, uniform='b')
            self.rowconfigure(2, weight=1, uniform='a')
            self.rowconfigure(3, weight=1, uniform='b')
            self.rowconfigure(4, weight=1, uniform='a')
            self.rowconfigure(5, weight=1, uniform='b')
            self.rowconfigure(6, weight=1, uniform='a')

        self.create_widgets(layout)

    def create_widgets(self, layout):
        test = zip(self.forecast_data, self.forecast_img)
        for widget in self.winfo_children():
            widget.destroy()

        if layout == 'bottom_vertical':
            for i in range(7):
                if i % 2 == 0:
                    (day_text, temp_text, weather_condition), img = next(test)
                    frm = ctk.CTkFrame(self, fg_color='transparent', corner_radius=20)
                    frm.grid(row=0, column=i, sticky='news')
                    ForecastCanvas(frm, img).pack(side='top', fill='x', anchor='center')
                    ctk.CTkLabel(frm, text=temp_text, font=(FONT, 18)).pack(side='top', expand=True)
                    ctk.CTkLabel(frm, text=day_text[:3], font=(FONT, 15)).pack(side='bottom', expand=True)
                else:
                    separator = ctk.CTkFrame(self, fg_color=self.seperator_color, width=3)
                    separator.grid(row=0, column=i, sticky='ns')
        if layout == 'horizontal on the right':
            for i in range(7):
                if i % 2 == 0:
                    (day_text, temp_text, weather_condition), img = next(test)
                    frm = ctk.CTkFrame(self, fg_color='transparent')
                    frm.grid(row=i, column=0, sticky='news')
                    ForecastCanvas(frm, img).pack(side='right', fill='both', padx=5)
                    ctk.CTkLabel(frm, text=temp_text, font=(FONT, 18), anchor='e', fg_color='transparent').pack(
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
