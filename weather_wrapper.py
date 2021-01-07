import requests
import json
from datetime import datetime
import calendar

LATITUDE = 0
LONGITUDE = 1
RESP = '{"coord":{"lon":34.7806,"lat":32.0809},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"base":"stations","main":{"temp":23,"feels_like":21.74,"temp_min":21.11,"temp_max":24,"pressure":1018,"humidity":41},"visibility":10000,"wind":{"speed":1.5,"deg":0},"clouds":{"all":0},"dt":1610019026,"sys":{"type":1,"id":6845,"country":"IL","sunrise":1609994540,"sunset":1610031094},"timezone":7200,"id":293397,"name":"Tel Aviv","cod":200}'

def get_current_utc_timestamp():
    current_datetime = datetime.datetime.utcnow()
    current_timetuple = current_datetime.utctimetuple()
    current_timestamp = calendar.timegm(current_timetuple)
    return current_timestamp

class WeatherAPI:
    API_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "d99bf122f85030a4283f57c7acab3de0"
    data = None

    def __init__(self, location):
        self.location = location

    def make_request(self):
        url = self.API_URL  # Inserting the url of the API
        url += "lat=" + str(self.location[LATITUDE])  # Inserting latitude of the location
        url += "&lon=" + str(self.location[LONGITUDE])  # Inserting longitude of the location
        url += "&appid=" + self.API_KEY  # Inserting API key of OpenWeather (unique)
        url += "&units=metric"  # Getting the units in the metric system (temp -> celsius)
        print(url)

        # Sending the request to the API
        # response = requests.get(self.API_URL)
        # print(response)
        # Deserialization with JSON
        self.data = json.loads(RESP)
        return self.data

    def get_main_attribute(self, attribute):
        return self.data['main'][attribute]

    def get_temp(self):
        return float(self.get_main_attribute('temp'))

    def get_humidity(self, timestamp=None):
        return float(self.get_main_attribute('humidity'))

    def get_visibility(self):
        return float(self.get_main_attribute('visibility'))

    def get_wind_speed(self):
        return float(self.data['wind']['speed'])

    def get_feels_like(self):
        return float(self.get_main_attribute('feels_like'))

    def get_extreme_weather(self):
        return self.data['weather'][0]['main']

    def get_weather_desc(self):
        return self.data['weather'][0]['description']

    def get_sunrise(self):
        return self.data['sys']['sunrise']

    def get_sunset(self):
        return self.data['sys']['sunset']


class WeatherWrapper:
    VEHICLE_EXTREME_WEATHER = ['Rain', 'Snow']
    MIN_VISIBILITY = 4000
    MIN_TEMP = 12
    MAX_TEMP = 38

    def __init__(self, weather):
        self.weather = weather

    def process_weather(self, forecast):
        # If result is negative, the priority is for pedestrians. Positive - vehicles
        temp = self.weather.get_temp()
        wind = self.weather.get_wind()
        sunset = self.weather.get_sunset()
        sunrise = self.weather.get_sunrise()
        extreme = self.weather.get_extreme()
        desc = self.weather.get_weather_desc()

        total_priority = 0

        if temp > self.MAX_TEMP:
            total_priority += -(self.MAX_TEMP - temp) / 10

        if temp < self.MIN_TEMP:
            total_priority += (self.MIN_TEMP - temp) / 10

        current_time = get_current_utc_timestamp()
        if sunset < current_time < sunrise:
            total_priority += (current_time - sunset) / 5

        if extreme in self.VEHICLE_EXTREME_WEATHER:
            total_priority += 10

        return total_priority


if __name__ == '__main__':
    w = WeatherAPI([32.08472326847056, 34.77643445486234])
    # Getting the closest forecast
    print(w.make_request())
    print(w.get_weather_desc())
    print(w.get_sunset())
