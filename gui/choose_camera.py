import tkinter as tk
from gui import new_camera
import gui.screen as screen


class ChooseCamera(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.cameras = self.database.get_cameras()

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(tuple(range(len(self.cameras) + 1)), weight=1)

        tk.Label(self, text="Select camera", font=(self.default_font, 64)).pack(pady=30)
        self.buttons = {}

        # TODO:This should be replaced with something similar to scroll view/list view
        for camera_id in self.cameras.keys():
            camera = self.cameras[camera_id]

            self.buttons[camera_id] = \
                tk.Button(self,
                          text=camera.get_name(),
                          command=lambda: self.choose_camera(camera_id),
                          font=(self.default_font, 20))
            self.buttons[camera.get_id()].pack(pady=10)

        tk.Button(self, text="Add a new camera", command=self.open_new_camera,
                  font=(self.default_font, 20)).pack(pady=30, side="bottom")

    def open_new_camera(self):
        self.controller.open_frame(new_camera.NewCamera)
        self.destroy_screen()

    def choose_camera(self, cam_id):
        self.controller.data["CAMERA"] = self.cameras[cam_id]
        self.destroy_screen()

