import tkinter as tk
import gui.screen as screen
from utils import CameraDetails as CameraDetails

class NewCamera(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.camera_label = tk.Label(text="New camera")
        self.camera_label.configure(font=("Courier", 44))
        self.camera_label.pack()

        self.fps_label = tk.Label(text="Frames per second")
        self.fps_label.configure(font=("Courier", 20))
        self.fps_label.pack()

        self.fps_box = tk.Entry(text="30")
        self.fps_box.configure(font=("Courier", 20))
        self.fps_box.pack()

        self.done_button = tk.Button(text="Done", command=self.register_camera)
        self.done_button.configure(font=("Courier", 30))
        self.done_button.pack()

    def register_camera(self):
        camera = CameraDetails(int(self.fps_box.get()))
        self.controller.data["CAMERA"] = camera
