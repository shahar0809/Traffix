import tkinter as tk
import gui.screen as screen
from gui import new_environment


class Home(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        #tk.Label(text="show environment").pack()
        #tk.Button()
        tk.Label(text="add environment").pack()
        tk.Button(text="", command=self.open_new_environment).pack()

    def open_new_environment(self):
        self.controller.open_frame(new_environment.NewEnvironment)
