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

        # Defining queues for input and output frames
        self.frames_queue = mp.Queue()
        self.results_queue = mp.Queue()

        # Getting the environment selected
        self.env = self.controller.data["ENVIRONMENT"]
        print("HELLOOO")
        print(self.database.get_camera_details(self.env.get_camera_id()).get_camera_index())

        tk.Button(self, text="Back", font=(self.default_font, 15),
                  command=self.go_back).pack(side="top", anchor="e")

        tk.Button(self, text="Update environment", font=(self.default_font, 20),
                  command=self.update_env).pack(anchor="w", side="top")

        # Adding title label
        tk.Label(self, text=self.env.get_name(), font=(self.default_font, 45)).pack(pady=10)

        # Initializing the logic module
        self.system = System(self.frames_queue, self.results_queue, self.env, self.database)

        # Initializing video feed panel widget an
        self.video_panel = None
        self.traffic_panel = None
        self.weather_panel = None

        self.system.run()
        self.vs = tk_video_stream.GuiVideoStream(self, self.controller, self.results_queue, self.stop_event)

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
