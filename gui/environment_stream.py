import tkinter as tk
from PIL import Image, ImageTk
from logic import System
import cv2
import multiprocessing as mp
import gui.screen as screen
import numpy as np
import os


class EnvironmentStream(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.image = None
        self.controller.attributes('-zoomed', False)

        # Defining indications
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.resources = os.path.join(self.root_dir, 'resources')

        self.green_light = self.convert_image(cv2.imread(os.path.join(self.resources, 'green.png')))
        self.red_light = self.convert_image(cv2.imread(os.path.join(self.resources, 'red.png')))

        # Defining queues for input and output frames
        self.frames_queue = mp.Queue()
        self.results_queue = mp.Queue()

        # Getting the environment selected
        self.env = self.controller.data["ENVIRONMENT"]

        # Adding title label
        tk.Label(self, text=self.env.get_name(), font=(self.default_font, 45)).pack(pady=20)

        # Initializing the logic module
        self.system = System(self.frames_queue, self.results_queue, self.env, self.database)

        # Initializing video feed panel widget an
        self.video_panel = None
        self.traffic_panel = None
        self.weather_panel = None

        # set a callback to handle when the window is closed
        self.controller.wm_title("Traffix")
        self.controller.wm_protocol("WM_DELETE_WINDOW", self.on_close)

        self.system.run()
        self.handle_process = mp.Process(target=self.handle_result_frames, args=(), daemon=True)
        self.handle_process.start()

    def on_close(self):
        self.system.on_close()

    @staticmethod
    def convert_image(image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        return image

    def handle_video_panel(self):
        self.image = self.convert_image(self.image)
        if self.video_panel is None:
            self.video_panel = tk.Label(image=self.image)
            self.video_panel.image = self.image
            self.video_panel.pack(side="left", padx=10, pady=10)
        else:
            self.video_panel.configure(image=self.image)
            self.video_panel.image = self.image

    def handle_traffic_light(self, decision):
        # Change light indication
        if decision:
            self.image = self.green_light
        else:
            self.image = self.red_light

        if self.traffic_panel is None:
            self.traffic_panel = tk.Label(image=self.image)
            self.traffic_panel.image = self.image
            self.traffic_panel.pack(side="left", padx=10, pady=10)
        else:
            self.traffic_panel.configure(image=self.image)
            self.traffic_panel.image = self.image

    def handle_result_frames(self):
        while not self.system.stop_event.is_set():
            print("hello")
            (res_frame, decision) = self.results_queue.get()
            print("DECISION")
            print(decision)

            # Change video feed frame
            self.image = res_frame
            self.handle_video_panel()

            self.handle_traffic_light(decision)
