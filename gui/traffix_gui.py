import tkinter as tk
from gui import choose_location, choose_camera, environment_stream, \
    home, new_camera, new_environment, set_traffic_bars, update_environment

windows = {
    "CHOOSE_CAMERA": choose_camera.ChooseCamera,
    "CHOOSE_LOCATION": choose_location.ChooseLocation,
    "ENV_STREAM": environment_stream.EnvironmentStream,
    "HOME": home.Home,
    "NEW_CAMERA": new_camera.NewCamera,
    "NEW_ENV": new_environment.NewEnvironment,
    "TRAFFIC_BARS": set_traffic_bars.SetTrafficBars,
    "UPDATE_ENV": update_environment.UpdateEnvironment
}


class TraffixGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.data = {}
        self.init_dict()

        self.open_frame(windows["HOME"])

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def open_frame(self, window):
        frame = window(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def init_dict(self):
        keys = ["CAMERA", "CROSSWALK", "LOCATION", "TRAFFIC_BARS", "CROSSWALK_WIDTH",
                "CROSSWALK_LENGTH", "ENVIRONMENT"]

        for key in keys:
            self.data[key] = None


def main():
    app = TraffixGUI()
    w = 800
    h = 650

    # get screen width and height
    ws = app.winfo_screenwidth()  # width of the screen
    hs = app.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen and where it is placed
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))
    app.mainloop()


if __name__ == '__main__':
    main()
