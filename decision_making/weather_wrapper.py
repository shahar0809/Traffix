import requests
import json
import datetime
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
        print(location)

    def make_request(self):
        url = self.API_URL  # Inserting the url of the API
        url += "lat=" + str(self.location[LATITUDE])  # Inserting latitude of the location
        url += "&lon=" + str(self.location[LONGITUDE])  # Inserting longitude of the location
        url += "&appid=" + self.API_KEY  # Inserting API key of OpenWeather (unique)
        url += "&units=metric"  # Getting the units in the metric system (temp -> celsius)
        print(url)

        # Sending the request to the API
        response = requests.get(url)
        # Deserialization with JSON
        self.data = response.json()
        return self.data

    def get_main_attribute(self, attribute):
        return self.data['main'][attribute]

    def get_temp(self):
        return float(self.get_main_attribute('temp'))

    def get_humidity(self, timestamp=None):
        return float(self.get_main_attribute('humidity'))

    def get_visibility(self):
        return float(self.data['visibility'])

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

    def get_weather_icon(self):
        return self.data['weather'][0]['icon']


class WeatherWrapper:
    VEHICLE_EXTREME_WEATHER = ['Rain', 'Snow']
    WEATHER_DESCRIPTIONS = ['snow', 'mist', 'rain', 'thunderstorm']
    MIN_VISIBILITY = 10000
    MAX_WIND_SPEED = 3

    def __init__(self, weather):
        self.weather = weather
        self.weather_indication = ""

        self.priorities = {'Heavy snow': 0.1, 'Heavy rain': 0.2, 'Light snow': 0.3, 'Low visibility': 0.5,
                           'Thunderstorm': 0.6, 'Mist': 0.5, 'Rain': 0.4, 'Light rain': 0.7, "Night": 0.8,
                           'Strong wind': 0.8, "": 1}

    def process_description(self):
        self.weather.make_request()
        self.weather_indication = ""
        desc = self.weather.get_weather_desc().lower()
        print("Desc" + desc)
        scalar = 1

        for weather in self.priorities.keys():
            if weather.lower() in desc:
                if self.priorities[weather] < self.priorities[self.weather_indication]:
                    self.weather_indication = weather
                scalar *= self.priorities[weather]

        return scalar

    def process_weather(self):
        desc_scalar = self.process_description()
        self.weather.make_request()

        wind = self.weather.get_wind_speed()
        sunset = self.weather.get_sunset()
        visibility = self.weather.get_visibility()

        dist_scalar = 1 * desc_scalar

        current_time = get_current_utc_timestamp()
        # If the current time is after sunset -> low visibility
        if sunset < current_time:
            # Dividing by a big number because of the UTC format
            delta = (current_time - sunset)
            dist_scalar *= (delta / 10 ** len(str(delta)))
            if self.priorities["Night"] < self.priorities[self.weather_indication]:
                self.weather_indication = "Night"

        if visibility < self.MIN_VISIBILITY:
            dist_scalar /= ((self.MIN_VISIBILITY - visibility) / 1000)
            if self.priorities["Low visibility"] < self.priorities[self.weather_indication]:
                self.weather_indication = "Low visibility"

        if wind > self.MAX_WIND_SPEED:
            dist_scalar /= (self.MAX_WIND_SPEED - wind)
            if self.priorities["Strong wind"] < self.priorities[self.weather_indication]:
                self.weather_indication = "Strong wind"

        return dist_scalar, self.weather_indication


if __name__ == '__main__':
    w = WeatherAPI([32.08472326847056, 34.77643445486234])
    # Getting the closest forecast
    print(w.make_request())
    print(w.get_weather_desc())
    print(w.get_sunset())
    wr = WeatherWrapper(w)
    print(wr.process_weather())
