import tkinter as tk
import gui.screen as screen
from tkinter import messagebox


class SetTrafficBars(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        info_text = ["Traffic bars are bars that define the loads of the environment.",
                     "There are 3 levels of traffic loads (low, medium, high).",
                     "the bars classify the amount of vehicles to a traffic load level."]

        # Define rows and columns in grid
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2, 3), weight=1)
        self.rowconfigure((4, 5, 6, 7), weight=2)
        self.bars = []

        tk.Label(self, text="Traffic bars", font=(self.default_font, 45)).grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Back", command=self.go_back,
                  font=(self.default_font, 15)).grid(row=0, column=0)
        tk.Label(self, text=info_text[0], font=(self.default_font, 14)).grid(row=1, column=0, columnspan=2)
        tk.Label(self, text=info_text[1], font=(self.default_font, 14)).grid(row=2, column=0, columnspan=2)
        tk.Label(self, text=info_text[2], font=(self.default_font, 14)).grid(row=3, column=0, columnspan=2)

        tk.Label(self, text="Low bar:", font=(self.default_font, 20)).grid(row=4, column=0)
        self.bars.append(tk.Entry(self, font=(self.default_font, 20)))

        tk.Label(self, text="Medium bar:", font=(self.default_font, 20)).grid(row=5, column=0)
        self.bars.append(tk.Entry(self, font=(self.default_font, 20)))

        tk.Label(self, text="High bar:", font=(self.default_font, 20)).grid(row=6, column=0)
        self.bars.append(tk.Entry(self, font=(self.default_font, 20)))

        # Pack entries for bars
        for i in range(3):
            self.bars[i].grid(row=i + 4, column=1)

        tk.Button(self, text="Done", font=(self.default_font, 25), command=self.update_bars_in_env). \
            grid(row=7, column=0, columnspan=2)

    def go_back(self):
        self.destroy_screen()

    def update_bars_in_env(self):
        bars = [int(bar.get()) for bar in self.bars]
        if not bars[0] < bars[1] < bars[2]:
            messagebox.showinfo(title="Error", message="The bars need to be sorted in ascending order!")
        else:
            self.controller.data["TRAFFIC_BARS"] = bars
            self.destroy_screen()
