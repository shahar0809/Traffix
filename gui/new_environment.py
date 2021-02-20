import tkinter as tk

class NewEnvironment(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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

        # Pack all components into window
        choose_camera_label.pack()
        choose_camera_button.pack()
        mark_crosswalk_label.pack()
        mark_crosswalk_button.pack()
        traffic_bars_label.pack()
        traffic_bars_button.pack()
        location_label.pack()
        location_button.pack()

    def open_choose_camera(self):
        pass

    def open_mark_crosswalk(self):
        pass

    def open_traffic_bars(self):
        pass

    def open_choose_location(self):
        pass
