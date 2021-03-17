import tkinter as tk
from PIL import Image, ImageTk
from logic import System
from queue import Queue
import cv2
import gui.screen as screen
import numpy as np
import os


class EnvironmentStream(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Defining indications

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        rsrc = os.path.join(ROOT_DIR, 'resources')
        print(os.path.join(rsrc, 'green.png'))

        im = cv2.imread(os.path.join(rsrc, 'green.png'))
        cv2.imshow('hi', im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        self.green_light = self.convert_image(cv2.imread(os.path.join(rsrc, 'green.png')))
        self.red_light = self.convert_image(cv2.imread(os.path.join(rsrc, 'red.png')))
        light_wid, light_height, channel = cv2.imread(os.path.join(rsrc, 'green.png')).shape

        # Defining queues for input and output frames
        self.frames_queue = Queue()
        self.results_queue = Queue()

        # Getting the environment selected
        self.env = self.controller.data["ENVIRONMENT"]

        # Adding title label
        tk.Label(self, text=self.env.get_name(), font=(self.default_font, 45)).pack(pady=20)

        # Initializing the logic module
        self.system = System(self.frames_queue, self.results_queue,
                             self.env, self.database)

        # Initializing video feed panel widget
        width, height = self.system.capture.get_dimensions()
        blank_image = np.zeros((height, width, 3), np.uint8)
        self.video_panel = tk.Label(image=blank_image)
        self.video_panel.image = blank_image
        self.video_panel.pack(side="left", padx=10, pady=10)

        # Initializing decision indication
        blank_image = np.zeros((light_height, light_wid, 3), np.uint8)
        self.traffic_panel = tk.Label(image=blank_image)
        self.traffic_panel.image = blank_image
        self.traffic_panel.pack(side="bottom", padx=10, pady=10)

        self.system.run()

    @staticmethod
    def convert_image(image):
        image = Image.fromarray(image)
        return ImageTk.PhotoImage(image)

    def handle_result_frames(self):
        while True:
            (res_frame, decision) = self.results_queue.get()

            # Change video feed frame
            res_frame = self.convert_image(res_frame)
            self.video_panel.configure(image=res_frame)
            self.video_panel.image = res_frame

            # Change light indication
            if decision:
                indication = self.green_light
            else:
                indication = self.red_light

            self.traffic_panel.configure(image=indication)
            self.traffic_panel.image = indication


class CustomCapture:
    def __init__(self, app, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        self.app = app
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        self.app.mainloop()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return False, None
