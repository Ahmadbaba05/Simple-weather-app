# weather_client.py
# This talks to the OpenWeatherMap API to get the weather data
# Ahmad is handling this file 

import re
import requests

from models import City, Forecast, ForecastDay
from models import InvalidCityNameError, CityNotFoundError, WeatherAPIError

BASE_URL = "https://api.openweathermap.org/data/2.5"

# city name should just be letters, spaces, hyphen or apostrophe, nothing weird
city_pattern = re.compile(r"^[A-Za-z\s\-']{2,50}$")


class WeatherClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def validate_city_name(self, raw_input):
        name = raw_input.strip()
        if not city_pattern.match(name):
            raise InvalidCityNameError("Please type a proper city name (letters only)")
        return name

    def get_current_weather(self, city_name):
        city_name = self.validate_city_name(city_name)
        url = BASE_URL + "/weather"
        params = {"q": city_name, "appid": self.api_key, "units": "metric"}

        try:
            response = requests.get(url, params=params, timeout=10)
        except Exception as e:
            raise WeatherAPIError("Network problem: " + str(e))

        if response.status_code == 404:
            raise CityNotFoundError("Could not find city: " + city_name)
        if response.status_code != 200:
            raise WeatherAPIError("Something went wrong, status code: " + str(response.status_code))

        data = response.json()

        try:
            city = City(
                data["name"],
                data["sys"]["country"],
                data["main"]["temp"],
                data["main"]["feels_like"],
                data["main"]["humidity"],
                data["wind"]["speed"],
                data["weather"][0]["description"].title(),
                data["weather"][0]["icon"],
                data["coord"]["lat"],
                data["coord"]["lon"],
            )
        except Exception as e:
            raise WeatherAPIError("Data from API looked weird: " + str(e))

        return city

    def get_forecast(self, city_name, days=5):
        city_name = self.validate_city_name(city_name)
        url = BASE_URL + "/forecast"
        params = {"q": city_name, "appid": self.api_key, "units": "metric"}

        try:
            response = requests.get(url, params=params, timeout=10)
        except Exception as e:
            raise WeatherAPIError("Network problem: " + str(e))

        if response.status_code == 404:
            raise CityNotFoundError("Could not find city: " + city_name)
        if response.status_code != 200:
            raise WeatherAPIError("Something went wrong, status code: " + str(response.status_code))

        data = response.json()
        forecast = Forecast(city_name)

        # group the 3 hour chunks the API gives us into one entry per day
        buckets = {}
        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0]
            temp = entry["main"]["temp"]
            condition = entry["weather"][0]["description"].title()
            icon = entry["weather"][0]["icon"]

            if date not in buckets:
                buckets[date] = {"min": temp, "max": temp, "condition": condition, "icon": icon}
            else:
                if temp < buckets[date]["min"]:
                    buckets[date]["min"] = temp
                if temp > buckets[date]["max"]:
                    buckets[date]["max"] = temp

        count = 0
        for date in buckets:
            if count >= days:
                break
            info = buckets[date]
            day = ForecastDay(date, info["min"], info["max"], info["condition"], info["icon"])
            forecast.add_day(day)
            count = count + 1

        return forecast
