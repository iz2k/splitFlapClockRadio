import json
from urllib import request

from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


class OpenWeatherMap:

    _apiKey = None
    _latitude = None
    _longitude = None

    def __init__(self, apiKey=None, latitude=None, longitude=None):
        if (apiKey != None):
            self.setApiKey(apiKey)
        if (latitude != None and longitude!= None):
            self.setLocation(latitude, longitude)

    def setApiKey(self, apiKey):
        self._apiKey = apiKey

    def setLocation(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude

    def getReport(self):
        url = 'https://api.openweathermap.org/data/2.5/onecall?'
        url = url + 'lat=' + str(self._latitude) + '&'
        url = url + 'lon=' + str(self._longitude) + '&'
        url = url + 'exclude=minutely&'
        url = url + 'units=metric&'
        url = url + 'lang=es&'
        url = url + 'appid=' + self._apiKey

        with request.urlopen(url) as con:
            return json.loads(con.read().decode())
