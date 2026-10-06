# models.py
# This file has the classes we use for weather info and our own errors
# Nathan (OOP + exception handling part)

class InvalidCityNameError(Exception):
    pass


class CityNotFoundError(Exception):
    pass


class WeatherAPIError(Exception):
    pass


class City:
    # holds the current weather for one city
    def __init__(self, name, country, temperature, feels_like, humidity, wind_speed, condition, icon_code, lat=0, lon=0):
        self.name = name
        self.country = country
        self.temperature = temperature
        self.feels_like = feels_like
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.condition = condition
        self.icon_code = icon_code
        self.lat = lat
        self.lon = lon

    def icon_url(self):
        return "https://openweathermap.org/img/wn/" + self.icon_code + "@2x.png"

    def summary(self):
        # just builds a simple text summary of the weather
        text = self.name + ", " + self.country + ": " + str(round(self.temperature, 1)) + "C"
        text = text + " (feels like " + str(round(self.feels_like, 1)) + "C), " + self.condition
        text = text + ", humidity " + str(self.humidity) + "%, wind " + str(self.wind_speed) + " m/s"
        return text


class ForecastDay:
    # one day inside the 5 day forecast
    def __init__(self, date, temp_min, temp_max, condition, icon_code):
        self.date = date
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.condition = condition
        self.icon_code = icon_code


class Forecast:
    # holds a list of ForecastDay objects for one city
    def __init__(self, city_name):
        self.city_name = city_name
        self.days = []

    def add_day(self, day):
        self.days.append(day)
