import requests
import json

LATITUDE = 0
LONGTITUDE = 1

class Weather:
    API_URL = "https://api.openweathermap.org/data/2.5/onecall?"
    API_KEY = "d99bf122f85030a4283f57c7acab3de0"
    data = None

    def __init__(self, location):
        self.location = location

    def make_request(self):
        url = self.API_URL + "lat=" + str(round(self.location[LATITUDE], 2)) +
        "&lon=" + str(round(self.location[LONGTITUDE], 2)) +
        "&appid=" + self.API_KEY


        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (self.location[LATITUDE], self.location[LONGTITUDE], self.API_KEY)
        response = requests.get(self.API_URL)
        self.data = json.loads(response.text)
        print(self.data)

    def get_temp(self):
        pass


if __name__ == '__main__':
    w = Weather([32.08472326847056, 34.77643445486234])
    w.make_request()
