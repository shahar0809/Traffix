import tkinter as tk
from gui import choose_location, choose_camera, environment_stream, \
    home, mark_crosswalk, new_camera, new_environment, set_traffic_bars, update_environment

windows = {
    "CHOOSE_CAMERA": choose_camera.ChooseCamera,
    "CHOOSE_LOCATION": choose_location.ChooseLocation,
    "ENV_STREAM": environment_stream.EnvironmentStream,
    "HOME": home.Home,
    "MARK_CROSSWALK": mark_crosswalk.MarkCrosswalk,
    "NEW_CAMERA": new_camera.NewCamera,
    "NEW_ENV": new_environment.NewEnvironment,
    "TRAFFIC_BARS": set_traffic_bars.SetTrafficBars,
    "UPDATE_ENV": update_environment.UpdateEnvironment
}


class TraffixGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.data = {}

        for window_name in windows.keys():
            frame = windows[window_name](container, self)
            self.frames[windows[window_name]] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(windows["NEW_ENV"])

    def open_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.deiconify()


def main():
    app = TraffixGUI()


if __name__ == '__main__':
    main()
