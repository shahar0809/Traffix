import os

import imutils
import tkinter as tk
from PIL import Image, ImageTk
from logic import System
import cv2
import multiprocessing as mp
import gui.screen as screen
import threading
from gui import tk_video_stream, update_environment, home


class EnvironmentStream(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.stop_event = threading.Event()
        self.image = None
        self.controller.attributes('-zoomed', False)
        self.interval = 10  # Interval in ms to get the latest frame
        self.weather_icons = {}
        self.priorities = {'Heavy snow': 0.1, 'Heavy rain': 0.2, 'Light snow': 0.4, 'Low visibility': 0.3,
                           'Thunderstorm': 0.5, 'Mist': 0.5, 'Rain': 0.5, 'Light rain': 0.7, "Night": 0.8,
                           'Strong wind': 0.8}

        # Defining queues for input and output frames
        self.frames_queue = mp.Queue()
        self.results_queue = mp.Queue()

        self.columnconfigure(0, weight=5)
        self.columnconfigure(0, weight=3)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        # Getting the environment selected
        self.env = self.controller.data["ENVIRONMENT"]

        tk.Button(self, text="Back", font=(self.default_font, 15),
                  command=self.go_back).grid(row=0, column=1, sticky="ne", padx=3, pady=3)

        tk.Button(self, text="Update environment", font=(self.default_font, 20),
                  command=self.update_env).grid(row=0, column=0, sticky="nw", padx=3, pady=3)

        # Adding title label
        tk.Label(self, text=self.env.get_name(), font=(self.default_font, 45)).grid(row=1, column=0, columnspan=2,
                                                                                    sticky="n", pady=(0, 20))

        self.curr_frame = None
        self.decision = False
        self.traffic_indication = None
        self.weather_label = None
        self.weather_indication = None
        self.weather_icon = None
        self.image_on_canvas = None
        self.traffic_panel = None

        self.tkFrame = tk.Frame(self, bd=2, relief=tk.SUNKEN, width=600, height=600)
        self.tkFrame.grid_rowconfigure(0, weight=1)
        self.tkFrame.grid_columnconfigure(0, weight=1)

        self.x_scroll = tk.Scrollbar(self.tkFrame, orient=tk.HORIZONTAL)
        self.x_scroll.grid(row=1, column=0, sticky=tk.E + tk.W)
        self.y_scroll = tk.Scrollbar(self.tkFrame)
        self.y_scroll.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.canvas = None

        # Defining indications
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.resources = os.path.join(self.root_dir, 'resources')

        self.green_light = cv2.imread(os.path.join(self.resources, 'green.png'))
        self.red_light = cv2.imread(os.path.join(self.resources, 'red.png'))

        self.green_light = imutils.resize(self.green_light, width=50, height=250)
        self.red_light = imutils.resize(self.red_light, width=50, height=250)

        self.green_light = self.convert_image(self.green_light)
        self.red_light = self.convert_image(self.red_light)
        self.define_weather_icons()

        # set a callback to handle when the window is closed
        self.controller.wm_title("Traffix Stream")
        self.controller.wm_protocol("WM_DELETE_WINDOW", self.on_close)

        # Initializing the logic module
        self.system = System(self.frames_queue, self.results_queue, self.env, self.database)

        # Initializing video feed panel widget an
        self.video_panel = None
        self.traffic_panel = None
        self.weather_panel = None
        self.controller.after(self.interval, self.update_canvas)
        self.system.run()

        # self.vs = tk_video_stream.GuiVideoStream(self, self.controller, self.results_queue, self.stop_event)

    def update_canvas(self):
        result = self.results_queue.get()

        if self.stop_event.is_set():
            return
        
        self.curr_frame = result[0]
        self.decision = result[1]
        self.weather_indication = result[2]
        print("IN STREAMMM")
        print(result[2])

        if self.decision:
            self.traffic_indication = self.green_light
        else:
            self.traffic_indication = self.red_light

        self.curr_frame = cv2.cvtColor(self.curr_frame, cv2.COLOR_BGR2RGB)
        self.curr_frame = Image.fromarray(self.curr_frame)
        self.curr_frame = ImageTk.PhotoImage(self.curr_frame)

        if self.canvas is not None:
            self.canvas.itemconfig(self.image_on_canvas, image=self.curr_frame)

        else:
            self.canvas = tk.Canvas(self.tkFrame, bd=0,
                                    width=600, height=600,
                                    xscrollcommand=self.x_scroll.set, yscrollcommand=self.y_scroll.set)
            self.canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
            self.x_scroll.config(command=self.canvas.xview)
            self.y_scroll.config(command=self.canvas.yview)
            self.image_on_canvas = self.canvas.create_image(0, 0, image=self.curr_frame, anchor="nw")
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
            self.tkFrame.grid(row=2, column=0, rowspan=5)

        if self.traffic_panel is None:
            self.traffic_panel = tk.Label(self, image=self.traffic_indication)
            self.traffic_panel.image = self.traffic_indication
            self.traffic_panel.grid(row=2, column=1)
        else:
            try:
                self.traffic_panel.configure(image=self.traffic_indication)
                self.traffic_panel.image = self.traffic_indication
            except Exception as e:
                print(e)

        if self.weather_panel is None:
            self.weather_icon = self.get_weather_icon(self.weather_indication)
            self.weather_panel = tk.Label(self, image=self.weather_icon)
            self.weather_panel.image = self.weather_icon
            self.weather_panel.pack_propagate(False)
            self.weather_panel.grid(row=3, column=1, padx=3)
            self.weather_label = tk.Label(self, text=self.weather_indication[0],
                                          font=(self.default_font, 10))
            self.weather_label.grid(row=4, column=1, padx=3)
        else:
            try:
                self.weather_panel.configure(image=self.weather_icon)
                self.weather_panel.image = self.weather_icon
                self.weather_label.config(text=self.weather_indication[0])
            except Exception as e:
                print(e)

        if not self.stop_event.is_set():
            self.controller.after(self.interval, self.update_canvas)

    def get_weather_icon(self, indication):
        indication = [desc.lower() for desc in indication]
        for weather in self.weather_icons.keys():
            weather_mode = weather.lower()
            print(weather_mode)
            print(indication)
            for desc in indication:
                if weather_mode in desc:
                    return self.weather_icons[weather]

    def define_weather_icons(self):
        self.weather_icons["RAIN"] = cv2.imread(os.path.join(self.resources, 'rain.png'))
        self.weather_icons["SNOW"] = cv2.imread(os.path.join(self.resources, 'snow.jpg'))
        self.weather_icons["THUNDERSTORM"] = cv2.imread(os.path.join(self.resources, 'thunderstorm.png'))
        self.weather_icons["VISIBILITY"] = cv2.imread(os.path.join(self.resources, 'visibility.png'))
        self.weather_icons["MIST"] = cv2.imread(os.path.join(self.resources, 'mist.png'))
        self.weather_icons["NIGHT"] = cv2.imread(os.path.join(self.resources, 'night.png'))
        self.weather_icons["WIND"] = cv2.imread(os.path.join(self.resources, 'wind.png'))

        for weather in self.weather_icons.keys():
            self.weather_icons[weather] = imutils.resize(self.weather_icons[weather], width=100, height=250)
            self.weather_icons[weather] = self.convert_image(self.weather_icons[weather])

    def on_close(self):
        self.stop_event.set()
        self.system.on_close()

    def update_env(self):
        self.on_close()
        self.pack_forget()
        self.destroy_screen()
        self.controller.data["ENV_ID"] = self.env.get_id()
        self.controller.open_frame(update_environment.UpdateEnvironment)

    def go_back(self):
        self.on_close()
        self.pack_forget()
        self.controller.open_frame(home.Home)
        self.destroy_screen()

    @staticmethod
    def convert_image(image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        return image
