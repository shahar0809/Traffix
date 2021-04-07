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
        self.interval = 2  # Interval in ms to get the latest frame

        # Defining queues for input and output frames
        self.frames_queue = mp.Queue()
        self.results_queue = mp.Queue()

        # Getting the environment selected
        self.env = self.controller.data["ENVIRONMENT"]
        print(self.database.get_camera_details(self.env.get_camera_id()).get_camera_index())

        tk.Button(self, text="Back", font=(self.default_font, 15),
                  command=self.go_back).pack(side="top", anchor="e")

        tk.Button(self, text="Update environment", font=(self.default_font, 20),
                  command=self.update_env).pack(anchor="w", side="top")

        # Adding title label
        tk.Label(self, text=self.env.get_name(), font=(self.default_font, 45)).pack(pady=10)

        self.curr_frame = None
        self.thread = None
        self.decision = False
        self.traffic_indication = None
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

        #self.vs = tk_video_stream.GuiVideoStream(self, self.controller, self.results_queue, self.stop_event)

    def update_canvas(self):
        result = self.results_queue.get()
        self.curr_frame = result[0]
        self.decision = result[1]

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
            self.tkFrame.pack(anchor="w", side="bottom")

        if self.traffic_panel is None:
            self.traffic_panel = tk.Label(self, image=self.traffic_indication)
            self.traffic_panel.image = self.traffic_indication
            self.traffic_panel.pack(anchor="s", side="right", padx=10, pady=10)

        # otherwise, simply update the panel
        else:
            try:
                self.traffic_panel.configure(image=self.traffic_indication)
                self.traffic_panel.image = self.traffic_indication
            except Exception as e:
                print(e)
        self.controller.after(self.interval, self.update_canvas)


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
        self.destroy_screen()
        self.controller.open_frame(home.Home)

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
