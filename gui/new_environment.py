import tkinter as tk
from gui import choose_camera, mark_crosswalk, set_traffic_bars, choose_location
from utils import Environment
from database import DB_Wrapper as database

class NewEnvironment(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.attributes = {"CAMERA": None, "CROSSWALK": None, "TRAFFIC_BARS": None, "LOCATION": None}

        # Camera section
        choose_camera_label = tk.Label(text="Choose camera:")
        choose_camera_button = tk.Button(text="camera", command=self.open_choose_camera)

        # Crosswalk section
        mark_crosswalk_label = tk.Label(text="Mark crosswalk:")
        mark_crosswalk_button = tk.Button(text="crosswalk", command=self.open_mark_crosswalk)

        # Traffic bars section
        traffic_bars_label = tk.Label(text="Choose traffic bars:")
        traffic_bars_button = tk.Button(text="traffic bars", command=self.open_traffic_bars)

        # Location coordinates section
        location_label = tk.Label(text="Choose location:")
        location_button = tk.Button(text="location", command=self.open_choose_location)

        done_button = tk.Button("DONE", command=self.insert_environment)

        # Pack all components into window
        choose_camera_label.pack()
        choose_camera_button.pack()
        mark_crosswalk_label.pack()
        mark_crosswalk_button.pack()
        traffic_bars_label.pack()
        traffic_bars_button.pack()
        location_label.pack()
        location_button.pack()
        done_button.pack()

    def open_choose_camera(self):
        self.controller.show_frame(choose_camera.ChooseCamera)

    def open_mark_crosswalk(self):
        self.controller.show_frame(mark_crosswalk.MarkCrosswalk)

    def open_traffic_bars(self):
        self.controller.show_frame(set_traffic_bars.SetTrafficBars)

    def open_choose_location(self):
        self.controller.show_frame(choose_location.ChooseLocation)

    def insert_environment(self):
        for attribute in self.attributes.keys():
            if self.attributes[attribute] is None:
                tk.messagebox.showinfo(title="Attention", message="Please fill all the attributes!")
                return

        env = Environment(self.attributes["CAMERA"],
                          self.attributes["CAMERA"].get_,
                          self.attributes["CAMERA"],
                          self.attributes["CAMERA"])


