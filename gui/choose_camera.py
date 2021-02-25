import tkinter as tk
import gui.screen as screen
from gui import new_camera


class ChooseCamera(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        nums = 3

        # for num in range(nums):
        # tk.Button(self, text="show camera", command=self).pack()

        tk.Button(self, text="add camera", command=self.open_new_camera).pack()

    def open_new_camera(self):
        self.controller.show_frame(new_camera.NewCamera)
        self.destroy()

