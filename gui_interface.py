import tkinter as tk
from tkinter import ttk
from uart_comm import *


class LightControl(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.red = tk.DoubleVar()
        self.blue = tk.DoubleVar()
        self.green = tk.DoubleVar()
        self.val = tk.DoubleVar()
        self.last_message = ''
        self.bottom_width = 12

        self.arduino = ArduinoSerial.set_serial()

        tk.Button(self,
                  text='RED',
                  width=self.bottom_width,
                  bg='red',
                  command=lambda: self.set_colors(255, 0, 0)
                  ).grid(column=0, row=1)

        tk.Button(self,
                  text='GREEN',
                  width=self.bottom_width,
                  bg='green',
                  command=lambda: self.set_colors(0, 255, 0)
                  ).grid(column=1, row=1)

        tk.Button(self,
                  text='BLUE',
                  width=self.bottom_width,
                  bg='blue',
                  fg='white',
                  command=lambda: self.set_colors(0, 0, 255)
                  ).grid(column=2, row=1)

        tk.Button(self,
                  text='COLD WHITE',
                  width=self.bottom_width,
                  bg='white',
                  command=lambda: self.set_colors(244, 253, 255)
                  ).grid(column=3, row=0)

        tk.Button(self,
                  text='WARM WHITE',
                  width=self.bottom_width,
                  bg='white',
                  command=lambda: self.set_colors(243, 231, 211)
                  ).grid(column=3, row=1)

        tk.Button(self,
                  text='YELLOW',
                  width=self.bottom_width,
                  bg='yellow',
                  command=lambda: self.set_colors(255, 255, 0)
                  ).grid(column=3, row=2, sticky=tk.N)

        tk.Button(self,
                  text='ON',
                  width=self.bottom_width,
                  bg='white',
                  command=lambda: self.turn_on()
                  ).grid(column=3, row=2, sticky=tk.S)

        tk.Button(self,
                  text='OFF',
                  width=self.bottom_width,
                  bg='black',
                  fg='white',
                  command=lambda: self.turn_off()
                  ).grid(column=3, row=3, sticky=tk.N)

        self.red_scale = tk.Scale(self, variable=self.red, from_=255, to=0, troughcolor='red',
                                  command=self.get_color_value)
        self.red_scale.grid(column=0, row=2)

        self.green_scale = tk.Scale(self, variable=self.green, from_=255, to=0, troughcolor='green',
                                    command=self.get_color_value)
        self.green_scale.grid(column=1, row=2)

        self.blue_scale = tk.Scale(self, variable=self.blue, from_=255, to=0, troughcolor='blue',
                                   command=self.get_color_value)
        self.blue_scale.grid(column=2, row=2)

        self.brightness_scale = tk.Scale(self, variable=self.val, from_=5, to=255, command=self.get_color_value,
                                         orient=tk.HORIZONTAL)
        self.brightness_scale.grid(column=1, row=3)

        bright_label = tk.Label(self, text='BRIGHTNESS')
        bright_label.grid(column=0, row=3)

        self.grid(padx=20, pady=20, sticky=tk.NSEW)

    def set_colors(self, *values):
        self.red_scale.set(values[0])
        self.green_scale.set(values[1])
        self.blue_scale.set(values[2])

    # def set_brightness(value):
    #     brightness_scale.set(value)

    def get_color_value(self, value):
        red_color = int(self.red.get() * self.brightness_scale.get() / 255)
        green_color = int(self.green.get() * self.brightness_scale.get() / 255)
        blue_color = int(self.blue.get() * self.brightness_scale.get() / 255)

        message = f'{red_color},{green_color},{blue_color}\n'
        if self.last_message != message:
            print(message)
            self.last_message = message
            self.arduino.write(message.encode())

    def turn_on(self):
        self.arduino.write(self.last_message.encode())

    def turn_off(self):
        self.arduino.write('0,0,0\n'.encode())


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Desk ambient lighting')

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.right_position = int((self.screen_width / 2) - 220)
        self.down_position = int((self.screen_height / 2) - 220)
        self.geometry(f'440x300+{self.right_position}+{self.down_position}')


if __name__ == '__main__':
    app = App()
    LightControl(app)
    app.mainloop()
