import customtkinter as ctk


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
                                      font=('Helvetica', 40))
        self.temp_date.grid(row=0, column=0, sticky='news')

        self.feels_label = ctk.CTkLabel(self,
                                        text=f'feels like: {self.feels_temp}',
                                        text_color=self.text_color,
                                        font=('Helvetica', 15)
                                        )
        self.feels_label.grid(row=1, column=0, sticky='news')
