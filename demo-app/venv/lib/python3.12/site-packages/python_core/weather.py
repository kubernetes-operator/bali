
import pyowm
from core.system import *

class OpenWeatherMap(object):
    def __init__(self):
        self.apikey = "20a03ca08eb464f1ac5f2ba9a4c01908"
        self.api = pyowm.OWM(self.apikey)

    def GetTemperature(self, location):
        """ How to use: self.GetTemperature("Skalborg")"""
        observation = self.api.weather_at_place(location)
        weather = observation.get_weather()
        temperature = weather.get_temperature('celsius')
        return "Weather in {}: ".format(location) + str(temperature['temp']) + "°C."


# usage
if __name__ == '__main__':
    instance = OpenWeatherMap()
    # print(instance.GetTemperature("Aalborg"))
    # print(instance.GetTemperature("Skalborg"))

    obj = instance.api.weather_at_place("Skalborg")
    w = obj.get_weather()
    print(dir(w))
    print(str(w.get_humidity()) + "% humidity")
    print(str(w.get_sunset_time()))
    print(w.get_weather_icon_url())
    print(w.to_JSON)