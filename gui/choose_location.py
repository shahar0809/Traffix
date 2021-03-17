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
        self.location = []

        self.weather = weather.WeatherAPI(self.location)

        tk.Label(self, text="Open google map:", font=(self.default_font, 50)).pack(pady=30)
        tk.Button(self, text="google map", command=self.open_google_map,
                  font=(self.default_font, 20)).place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        tk.Label(self, text="Latitude:", font=(self.default_font, 20)).grid(row=4, column=0)
        self.location.append(tk.Entry(self, font=(self.default_font, 20)))

        tk.Label(self, text="Longitude:", font=(self.default_font, 20)).grid(row=5, column=0)
        self.location.append(tk.Entry(self, font=(self.default_font, 20)))

        # Pack entries for location
        for i in range(2):
            self.location[i].grid(row=i + 4, column=1)

        tk.Button(self, text="Done", font=(self.default_font, 25), command=self.choose_location). \
            grid(row=7, column=0, columnspan=2)

    def open_google_map(self):
        webbrowser.open("https://www.google.co.il/maps")

    def choose_location(self):
        location = [location.get() for location in self.location]
        self.controller.data["LOCATION"] = location
        self.destroy_screen()



