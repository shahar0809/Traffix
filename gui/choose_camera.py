import tkinter as tk
from gui import new_camera
import gui.screen as screen


class ChooseCamera(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        tk.Label(self, text="Select camera", font=(self.default_font, 64)).pack(pady=30)
        nums = 3

        for num in range(nums):
            tk.Button(self, text="Show camera", command=self.open_new_camera,
                      font=(self.default_font, 20)).pack(pady=10)

        tk.Button(self, text="Add an environment", command=self.open_new_camera,
                  font=(self.default_font, 20)).pack(pady=30, side="bottom")

    def open_new_camera(self):
        self.controller.open_frame(new_camera.NewCamera)

