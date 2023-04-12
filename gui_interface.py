import customtkinter as ctk
import tkinter as tk
from uart_comm import *


class App(ctk.CTk):
    """
        Class with main application window
    """
    def __init__(self):
        super().__init__()

        self.title('Desk ambient lighting')

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.right_position = int((self.screen_width / 2) - 220)
        self.down_position = int((self.screen_height / 2) - 220)
        self.geometry(f'500x300+{self.right_position}+{self.down_position}')


class LightControl(ctk.CTkFrame):
    """
        Class with all the equipment and methods for lighting control
    """
    def __init__(self, container):
        super().__init__(container)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.red = tk.DoubleVar()
        self.blue = tk.DoubleVar()
        self.green = tk.DoubleVar()
        self.val = tk.DoubleVar()
        self.last_message = ''
        self.message = ''
        self.red_color = 0
        self.green_color = 0
        self.blue_color = 0
        self.bottom_width = 110
        self.slider_height = 120

        self.arduino = ArduinoSerial.set_serial()

        ctk.CTkButton(self,
                      text='RED',
                      width=self.bottom_width,
                      fg_color='red',
                      hover_color='darkred',
                      command=lambda: self.set_sliders(255, 0, 0)
                      ).grid(column=0, row=1)

        ctk.CTkButton(self,
                      text='GREEN',
                      width=self.bottom_width,
                      fg_color='green',
                      hover_color='darkgreen',
                      command=lambda: self.set_sliders(0, 255, 0)
                      ).grid(column=1, row=1)

        ctk.CTkButton(self,
                      text='BLUE',
                      width=self.bottom_width,
                      fg_color='blue',
                      hover_color='darkblue',
                      command=lambda: self.set_sliders(0, 0, 255)
                      ).grid(column=2, row=1)

        ctk.CTkButton(self,
                      text='COLD WHITE',
                      width=self.bottom_width,
                      fg_color='white',
                      hover_color='lightgray',
                      text_color='black',
                      command=lambda: self.set_sliders(244, 253, 255)
                      ).grid(column=3, row=0)

        ctk.CTkButton(self,
                      text='WARM WHITE',
                      width=self.bottom_width,
                      fg_color='white',
                      hover_color='lightgray',
                      text_color='black',
                      command=lambda: self.set_sliders(243, 231, 211)
                      ).grid(column=3, row=1)

        ctk.CTkButton(self,
                      text='YELLOW',
                      width=self.bottom_width,
                      fg_color='yellow',
                      hover_color='lightgray',
                      text_color='black',
                      command=lambda: self.set_sliders(255, 255, 0)
                      ).grid(column=3, row=2, sticky=tk.N)

        ctk.CTkButton(self,
                      text='ON',
                      width=self.bottom_width,
                      fg_color='white',
                      hover_color='lightgray',
                      text_color='black',
                      command=lambda: self.turn_on()
                      ).grid(column=3, row=2, sticky=tk.S)

        ctk.CTkButton(self,
                      text='OFF',
                      width=self.bottom_width,
                      fg_color='black',
                      hover_color='gray',
                      text_color='lightgray',
                      command=lambda: self.turn_off()
                      ).grid(column=3, row=3, sticky=tk.N)

        self.red_scale = ctk.CTkSlider(self,
                                       variable=self.red,
                                       from_=0,
                                       to=255,
                                       height=120,
                                       fg_color='darkred',
                                       progress_color='red',
                                       orientation='vertical',
                                       command=self.set_colors)
        self.red_scale.grid(column=0, row=2)

        self.green_scale = ctk.CTkSlider(self,
                                         variable=self.green,
                                         from_=0,
                                         to=255,
                                         height=self.slider_height,
                                         fg_color='darkgreen',
                                         progress_color='green',
                                         orientation='vertical',
                                         command=self.set_colors)
        self.green_scale.grid(column=1, row=2)

        self.blue_scale = ctk.CTkSlider(self,
                                        variable=self.blue,
                                        from_=0,
                                        to=255,
                                        height=self.slider_height,
                                        fg_color='darkblue',
                                        progress_color='blue',
                                        orientation='vertical',
                                        command=self.set_colors)
        self.blue_scale.grid(column=2, row=2)

        self.brightness_scale = ctk.CTkSlider(self,
                                              variable=self.val,
                                              from_=5,
                                              to=255,
                                              width=self.slider_height,
                                              fg_color='gray',
                                              progress_color='lightgray',
                                              orientation='horizontal',
                                              command=self.set_colors)
        self.brightness_scale.grid(column=1, row=4)

        bright_label = ctk.CTkLabel(self, text='BRIGHTNESS')
        bright_label.grid(column=0, row=4)

        self.error_label = ctk.CTkLabel(self, text='', text_color='red')
        self.error_label.grid(column=1, row=5)

        self.grid(padx=25, pady=20, sticky=tk.NSEW)

    def set_sliders(self, *values):
        """
            Method for setting sliders in the right position
        Parameters
        ----------
        values: int
            Values corresponding to the colors in order: red, green, blue
        Returns
        -------

        """
        self.red_scale.set(values[0])
        self.green_scale.set(values[1])
        self.blue_scale.set(values[2])
        self.set_colors(0)

    def set_colors(self, value):
        """
            Method for setting variables storing color values including brightness
        Parameters
        ----------
        value
            Empty argument for proper operation of the function called by the slider
        Returns
        -------

        """
        self.red_color = int(self.red.get() * self.brightness_scale.get() / 255)
        self.green_color = int(self.green.get() * self.brightness_scale.get() / 255)
        self.blue_color = int(self.blue.get() * self.brightness_scale.get() / 255)
        self._create_message()

    def _create_message(self):
        """
            Method that generates a message that will be sent via uart to the arduino driver
        Returns
        -------

        """
        message = f'{self.red_color},{self.green_color},{self.blue_color}\n'
        if self.last_message != message:
            # print(message)
            self.last_message = message
            self._send_message(message)

    def turn_on(self):
        """
            Method that sends the last saved message
        Returns
        -------

        """
        self._send_message(self.last_message)

    def turn_off(self):
        """
            Method that send message to turn off all LEDs (0, 0, 0)
        Returns
        -------

        """
        self._send_message('0,0,0\n')

    def _send_message(self, message):
        """
            Method for sending message to arduino. If the arduino is not connected, an appropriate message
            will appear in the application
        Parameters
        ----------
        message: str
            Message containing information on what values to set the appropriate color channels with
        Returns
        -------

        """
        try:
            self.arduino.write(message.encode())
            self.error_label.configure(text='')
        except AttributeError:
            self.error_label.configure(text="I can't find an arduino")


if __name__ == '__main__':
    app = App()
    LightControl(app)
    app.mainloop()
