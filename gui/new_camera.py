import tkinter as tk
import gui.screen as screen
from utils import CameraDetails as CameraDetails
from gui import choose_camera as choose_camera


class NewCamera(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(self, text="Register new camera", font=(self.default_font, 45)).pack(pady=(30, 50))
        tk.Label(self, text="Camera name:", font=(self.default_font, 20)).pack(pady=10)
        self.name_box = tk.Entry(self, text="new camera", font=(self.default_font, 20))
        self.name_box.pack(pady=(0, 20))

        tk.Label(self, text="Frames per second:", font=(self.default_font, 20)).pack(pady=10)
        self.fps_box = tk.Entry(self, text="30", font=(self.default_font, 20))
        self.fps_box.pack(pady=(0, 20))

        tk.Button(self, text="Done", font=(self.default_font, 30), command=self.register_camera).\
            pack(side="bottom", pady=(0, 30))

    def register_camera(self):
        self.database.add_camera_details(str(self.name_box.get()), int(self.fps_box.get()), 0)
        self.destroy_screen()
        self.controller.open_frame(choose_camera.ChooseCamera)
