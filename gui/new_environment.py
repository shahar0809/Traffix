import tkinter as tk
from gui import choose_camera, mark_crosswalk, set_traffic_bars, choose_location
from utils import Environment
import gui.screen as Screen


class NewEnvironment(Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Camera section
        tk.Label(text="Choose camera:").pack()
        tk.Button(text="camera", command=self.open_choose_camera).pack()

        # Crosswalk section
        tk.Label(text="Mark crosswalk:").pack()
        tk.Button(text="crosswalk", command=self.open_mark_crosswalk).pack()

        # Traffic bars section
        tk.Label(text="Choose traffic bars:").pack()
        tk.Button(text="traffic bars", command=self.open_traffic_bars).pack()

        # Location coordinates section
        tk.Label(text="Choose location:").pack()
        tk.Button(text="location", command=self.open_choose_location).pack()

        tk.Button("DONE", command=self.insert_environment).pack()

    def open_choose_camera(self):
        self.controller.open_frame(choose_camera.ChooseCamera)

    def open_mark_crosswalk(self):
        self.controller.open_frame(mark_crosswalk.MarkCrosswalk)

    def open_traffic_bars(self):
        self.controller.open_frame(set_traffic_bars.SetTrafficBars)

    def open_choose_location(self):
        self.controller.open_frame(choose_location.ChooseLocation)

    def insert_environment(self):
        for attribute in self.attributes.keys():
            if self.attributes[attribute] is None:
                tk.messagebox.showinfo(title="Attention", message="Please fill all the attributes!")
                return

        env = Environment(self.controller.data["CAMERA"],
                          self.controller.data["CROSSWALK"],
                          self.controller.data["TRAFFIC_BARS"],
                          self.controller.data["LOCATION"])

        self.database.add_environment(env)
