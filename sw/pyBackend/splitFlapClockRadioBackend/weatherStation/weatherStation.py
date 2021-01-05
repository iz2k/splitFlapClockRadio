import json
from datetime import datetime

from splitFlapClockRadioBackend.weatherStation.bme680.simpleBme680 import SimpleBME680
from splitFlapClockRadioBackend.weatherStation.sgp30.simpleSgp30 import SimpleSGP30
from splitFlapClockRadioBackend.weatherStation.openWeatherMap.openWeatherMap import OpenWeatherMap
from splitFlapClockRadioBackend.dbManager import Measurement, CityMeas, HomeMeas
from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.tools.jsonTools import writeJsonFile, readJsonFile, prettyJson


class WeatherStation:

    config = {}
    weatherReport = {}
    sensorReport = {}

    bme = None
    sgp = None
    openWeather = None

    def __init__(self, dbctl : dbController):
        self.loadConfig()
        #self.printConfig()
        self.bme = SimpleBME680()
        self.sgp = SimpleSGP30([int(self.config['baselineEco2']), int(self.config['baselineTvoc'])])
        self.openWeather = OpenWeatherMap(apiKey=self.config['openWeatherApi'],
                                          latitude=self.config['latitude'],
                                          longitude=self.config['longitude'])
        self.dbctl = dbctl

    def saveConfig(self):
        writeJsonFile('cfgWeatherStation.json', self.config)

    def loadConfig(self):
        self.config = readJsonFile('cfgWeatherStation.json')
        if self.config == {}:
            self.createDefaultConfig()

    def reloadConfig(self):
        self.loadConfig()
        self.printConfig()
        self.sgp.resetDevice()
        self.sgp.initConfig([int(self.config['baselineEco2']), int(self.config['baselineTvoc'])])


    def printConfig(self):
        print('Weather Station Config:')
        print(prettyJson(self.config))

    def createDefaultConfig(self):
        self.config = {
            'openWeatherApi': '***REMOVED***',
            'geocodeApi': '',
            'location': '',
            'cityAlias': '',
            'longitude': 0,
            'latitude': 0,
            'baselineEco2': 34274,
            'baselineTvoc': 34723
                       }
        self.saveConfig()

    def updateParam(self, param, value):
        self.config[param]=value
        self.saveConfig()

    def updateWeatherReport(self):
        self.weatherReport = self.openWeather.getReport()
        print('[WeatherStation] Report Update:')
        print(prettyJson(
            {
                'location' : self.config['location'],
                'temperature' : str(self.weatherReport['current']['temp']) + 'C',
                'pressure' : str(self.weatherReport['current']['pressure']) + 'mbar',
                'humidity' : str(self.weatherReport['current']['humidity']) + '%',
                'weather' : self.weatherReport['current']['weather'][0]['description']
            }
        ))

    def updateSensorReport(self):
        self.sensorReport = {}
        bmedata = {}
        while bmedata == {}:
            bmedata = self.bme.getSensorData()

        for parameter in bmedata:
            self.sensorReport[parameter] = bmedata[parameter]
        sgpdata = self.sgp.getSensorData()
        for parameter in sgpdata:
            self.sensorReport[parameter] = sgpdata[parameter]
        #print(self.sensorReport)

    def insertToDb(self):
        myMeas = Measurement(
            datetime=datetime.now(),
            cityMeas=CityMeas(
                location=self.config['location'],
                temperature=self.weatherReport['current']['temp'],
                pressure=self.weatherReport['current']['pressure'],
                humidity=self.weatherReport['current']['humidity'],
                uvi=self.weatherReport['current']['uvi'],
                wind_speed=self.weatherReport['current']['wind_speed'],
                wind_degree=self.weatherReport['current']['wind_deg'],
                pop=self.weatherReport['hourly'][0]['pop']
            ),
            homeMeas=HomeMeas(
                temperature=self.sensorReport['temperature'],
                pressure=self.sensorReport['pressure'],
                humidity=self.sensorReport['humidity'],
                gas_resistance=self.sensorReport['gas_resistance'],
                eco2=self.sensorReport['eCO2'],
                tvoc=self.sensorReport['TVOC']
            )
        )

        self.dbctl.insert(myMeas)

    def get_ww_idx(self):
        dictionary = {
            '01d' : 0,
            '01n' : 1,
            '02d' : 2,
            '02n' : 3,
            '03d' : 4,
            '03n' : 4,
            '04d' : 5,
            '04n' : 5,
            '09d' : 8,
            '09n' : 8,
            '10d' : 6,
            '10n' : 7,
            '11d' : 9,
            '11n' : 9,
            '13d' : 11,
            '13n' : 11,
            '50d' : 10,
            '50n' : 10,
        }
        return dictionary[self.weatherReport['current']['weather'][0]['icon']]
