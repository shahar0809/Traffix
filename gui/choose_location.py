import tkinter as tk
import gui.screen as screen
import webbrowser
import decision_making.weather_wrapper as weather


class ChooseLocation(screen.Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2, 3), weight=1)
        self.rowconfigure((4, 5, 6, 7), weight=2)

        self.weather = weather.WeatherAPI(self.location)

        tk.Label(self, text="Choose location", font=(self.default_font, 50)).grid(row=0, column=0, columnspan=2)
        tk.Button(self, text="Google maps", command=self.open_google_maps,
                  font=(self.default_font, 20)).grid(row=1, column=0, columnspan=2)

        tk.Label(self, text="Copy the latitude and longitude", font=(self.default_font, 14)).grid(row=2, column=0, columnspan=2)

        tk.Label(self, text="Location:", font=(self.default_font, 20)).grid(row=3, column=0)
        self.location = tk.Entry(self, font=(self.default_font, 20))
        self.location.grid(row=3, column=1)

        tk.Button(self, text="Done", font=(self.default_font, 25), command=self.choose_location). \
            grid(row=4, column=0, columnspan=2)

    def open_google_maps(self):
        webbrowser.open("https://www.google.co.il/maps")

    def choose_location(self):
        location = self.location.get().split(", ")
        self.controller.data["LOCATION"] = location
        self.destroy_screen()



