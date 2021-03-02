import tkinter as tk
import gui.screen as screen


class SetTrafficBars(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        info_text = "Traffic bars are bars that define the loads of the environment." \
                    "There are 3 levels of traffic loads (low, medium, high), and the bars classify" \
                    " the amount of vehicles to a traffic load level."

        # Define rows and columns in grid
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure((1, 2, 3, 4, 5), weight=1)
        self.bars = []

        tk.Label(self, text="Traffic bars", font=(self.default_font, 45)).grid(row=0, column=0, columnspan=2)
        tk.Label(self, text=info_text, font=(self.default_font, 18)).grid(row=1, column=0, columnspan=2)

        tk.Label(self, text="Low bar:", font=(self.default_font, 20)).grid(row=2, column=0)
        self.bars += tk.Entry(self, font=(self.default_font, 20))

        tk.Label(self, text="Medium bar:", font=(self.default_font, 20)).grid(row=3, column=0)
        self.bars += tk.Entry(self, font=(self.default_font, 20))

        tk.Label(self, text="High bar:", font=(self.default_font, 20)).grid(row=4, column=0)
        self.bars += tk.Entry(self, font=(self.default_font, 20))

        # Pack entries for bars
        for i in range(3):
            self.bars[i].grid(row=i + 2, column=1)

        tk.Button(self, text="Done", font=(self.default_font, 25), command=self.update_bars_in_env). \
            grid(row=5, column=0, columnspan=2)

    def update_bars_in_env(self):
        self.controller.data["TRAFFIC_BARS"] = [int(bar.get()) for bar in self.bars]
        self.destroy_screen()
