import tkinter as tk
import gui.screen as screen
from utils import CameraDetails as CameraDetails

class NewCamera(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(text="New camera").config(font=("Courier", 44)).pack()
        tk.Label(text="Frames per second").config(font=("Courier", 20)).pack()
        self.fps_box = tk.Entry(text="30").config(font=("Courier", 20))
        self.fps_box.pack()

        tk.Button(text="Done", command=self.register_camera).config(font=("Courier", 30)).pack()

    def register_camera(self):
        camera = CameraDetails(int(self.fps_box.get()))
        self.controller.data["CAMERA"] = camera
