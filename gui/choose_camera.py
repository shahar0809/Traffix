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

        # TODO:This should be replaced with something similar to scroll view/list view
        for num in range(nums):
            # TODO: The text of each button should be the name of the camera + id
            # TODO: Command needs to add camera to data in controller and destroy screen
            tk.Button(self, text="Choose camera " + str(num), command=self.open_new_camera,
                      font=(self.default_font, 20)).pack(pady=10)

        tk.Button(self, text="Add a new camera", command=self.open_new_camera,
                  font=(self.default_font, 20)).pack(pady=30, side="bottom")

    def open_new_camera(self):
        self.controller.open_frame(new_camera.NewCamera)

