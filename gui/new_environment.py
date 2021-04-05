import tkinter as tk
from tkinter import messagebox
from gui import choose_camera, crosswalk_details, set_traffic_bars, choose_location, home
import gui.screen as screen


class NewEnvironment(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.parent = parent

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        tk.Label(self, text="Register environment", font=(self.default_font, 45)).grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Back", command=self.go_back,
                  font=(self.default_font, 20)).grid(row=0, column=0, padx=(10, 0), ipadx=2)
        # Name section
        tk.Label(self, text="Name:", font=(self.default_font, 20)). \
            grid(row=1, column=0, padx=30, sticky='w')
        self.name = tk.Entry(self, font=(self.default_font, 20))
        self.name.grid(row=1, column=1, padx=(0, 30), ipadx=8)

        # Camera section
        tk.Label(self, text="Choose camera:", font=(self.default_font, 20)). \
            grid(row=2, column=0, padx=30, sticky='w')
        tk.Button(self, text="camera", command=self.open_choose_camera,
                  font=(self.default_font, 20)).grid(row=2, column=1, padx=(0, 30), ipadx=8)

        # Crosswalk section
        tk.Label(self, text="Mark crosswalk:", font=(self.default_font, 20)).\
            grid(row=3, column=0, padx=30, sticky='w')
        tk.Button(self, text="crosswalk", command=self.open_mark_crosswalk,
                  font=(self.default_font, 20)).grid(row=3, column=1, padx=(0, 30), ipadx=8)

        # Traffic bars section
        tk.Label(self, text="Choose traffic bars:", font=(self.default_font, 20)).\
            grid(row=4, column=0, padx=30, sticky='w')
        tk.Button(self, text="traffic bars", command=self.open_traffic_bars,
                  font=(self.default_font, 20)).grid(row=4, column=1, padx=(0, 30), ipadx=8)

        # Location coordinates section
        tk.Label(self, text="Choose location:", font=(self.default_font, 20)).\
            grid(row=5, column=0, padx=30, sticky='w')
        tk.Button(self, text="location", command=self.open_choose_location,
                  font=(self.default_font, 20)).grid(row=5, column=1, padx=(0, 30), ipadx=8)

        tk.Button(self, text="DONE", font=(self.default_font, 30), command=self.insert_environment). \
            grid(row=6, column=0, columnspan=2, pady=30)

    def open_choose_camera(self):
        self.controller.open_frame(choose_camera.ChooseCamera)

    def open_mark_crosswalk(self):
        if self.controller.data["CAMERA"] is None:
            messagebox.showerror(title="Error", message="Please choose a camera")
        else:
            self.controller.open_frame(crosswalk_details.CrosswalkDetails)

    def go_back(self):
        self.controller.open_frame(home.Home)

    def open_traffic_bars(self):
        self.controller.open_frame(set_traffic_bars.SetTrafficBars)

    def open_choose_location(self):
        self.controller.open_frame(choose_location.ChooseLocation)

    def insert_environment(self):
        attributes = [self.controller.data["CAMERA"],
                      self.controller.data["CROSSWALK"],
                      self.controller.data["TRAFFIC_BARS"],
                      self.controller.data["LOCATION"]]

        print(attributes)

        is_env_ready = self.name.get() != ""
        for attribute in attributes:
            if attribute is None:
                is_env_ready = False

        if is_env_ready:
            self.database.add_environment(str(self.name.get()), self.controller.data["CAMERA"].get_id(),
                                          self.controller.data["CROSSWALK"], self.controller.data["TRAFFIC_BARS"],
                                          self.controller.data["LOCATION"])
            self.controller.open_frame(home.Home)
        else:
            messagebox.showinfo(title="Attention", message="Please fill all the attributes!")
