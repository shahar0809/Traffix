import tkinter as tk
import gui.screen as screen
from gui import mark_crosswalk


class CrosswalkDetails(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        tk.Label(self, text="Crosswalk details", font=(self.default_font, 45)).grid(row=0, column=0, columnspan=2)

        tk.Label(self, text="Width (cm):", font=(self.default_font, 20)). \
            grid(row=1, column=0, padx=30, sticky='w')
        self.width_box = tk.Entry(self, font=(self.default_font, 20))
        self.width_box.grid(row=1, column=1, padx=(0, 30), ipadx=8)

        tk.Label(self, text="Length (cm):", font=(self.default_font, 20)). \
            grid(row=2, column=0, padx=30, sticky='w')
        self.length_box = tk.Entry(self, font=(self.default_font, 20))
        self.length_box.grid(row=2, column=1, padx=(0, 30), ipadx=8)

        tk.Button(self, text="MARK", font=(self.default_font, 30), command=self.show_next_screen). \
            grid(row=3, column=0, columnspan=2, pady=20)

        tk.Button(self, text="DONE", font=(self.default_font, 30), command=self.back). \
            grid(row=4, column=0, columnspan=2, pady=10)

    def show_next_screen(self):
        self.controller.data["CROSSWALK_WIDTH"] = int(self.width_box.get())
        self.controller.data["CROSSWALK_LENGTH"] = int(self.length_box.get())
        self.controller.open_frame(mark_crosswalk.MarkCrosswalk)

    def back(self):
        self.destroy_screen()
