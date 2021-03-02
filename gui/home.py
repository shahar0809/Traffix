import tkinter as tk
import gui.screen as screen
from gui import new_environment, environment_stream


class Home(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(self, text="Traffix", font=(self.default_font, 64)).pack(pady=30)
        nums = 3
         # TODO:This should be replaced with something similar to scroll view/list view
        for num in range(nums):
            # TODO: The text of each button should be the name of the camera + id
            # TODO: Command needs to add camera to data in controller and destroy screen
            tk.Button(self, text="Show an environment", command=self.open_environment_stream,
                      font=(self.default_font, 20)).pack(pady=10)

        tk.Button(self, text="Add an environment", command=self.open_new_environment,
                  font=(self.default_font, 20)).pack(pady=30, side="bottom")

    def open_new_environment(self):
        self.controller.open_frame(new_environment.NewEnvironment)

    def open_environment_stream(self):
        self.controller.open_frame(environment_stream.EnvironmentStream)
