import tkinter as tk
import gui.screen as screen
from gui import new_environment, environment_stream


class Home(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        nums = 3

        tk.Label(self, text="Welcome").pack()

        for num in range(nums):
            tk.Button(self, text="show environment", command=self.open_environment_stream).pack()

        tk.Button(self, text="add environment", command=self.open_new_environment).pack()

    def open_new_environment(self):
        self.controller.show_frame(new_environment.NewEnvironment)
        self.destroy()

    def open_environment_stream(self):
        self.destroy()
        self.controller.show_frame(environment_stream.EnvironmentStream)