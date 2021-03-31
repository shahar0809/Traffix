import tkinter as tk
import gui.screen as screen
from gui import new_environment, environment_stream
from tkinter.ttk import *
event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))


class Home(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.envs = self.database.get_environments()
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(tuple(range(len(self.envs) + 1)), weight=1)

        tk.Label(self, text="Traffix", font=(self.default_font, 64)).pack(pady=30)
        self.buttons = {}

        for env_id in self.envs.keys():
            env = self.envs[env_id]

            self.buttons[env_id] = \
                tk.Button(self,
                          text=env.get_name(),
                          command=lambda: self.choose_env(env_id),
                          font=(self.default_font, 20))
            self.buttons[env.get_id()].pack(pady=10)

        tk.Button(self, text="Add an environment", command=self.open_new_environment,
                  font=(self.default_font, 20)).pack(pady=30, side="bottom")

    def open_new_environment(self):
        self.controller.open_frame(new_environment.NewEnvironment)

    def choose_env(self, env_id):
        self.controller.data["ENVIRONMENT"] = self.envs[env_id]
        self.destroy_screen()
        self.controller.open_frame(environment_stream.EnvironmentStream)
