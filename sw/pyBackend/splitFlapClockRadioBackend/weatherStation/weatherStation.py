import json
from datetime import datetime

from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.weatherStation.bme680.simpleBme680 import SimpleBME680
from splitFlapClockRadioBackend.weatherStation.sgp30.simpleSgp30 import SimpleSGP30
from splitFlapClockRadioBackend.weatherStation.openWeatherMap.openWeatherMap import OpenWeatherMap
from splitFlapClockRadioBackend.dbManager import Measurement, CityMeas, HomeMeas
from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.tools.jsonTools import writeJsonFile, readJsonFile, prettyJson


class WeatherStation:

    config : Config = None
    weatherReport = {}
    sensorReport = {}

    bme = None
    sgp = None
    openWeather = None

    def __init__(self, dbctl : dbController, config : Config):
        self.dbctl = dbctl
        self.config = config
        self.bme = SimpleBME680()
        self.sgp = SimpleSGP30([int(self.config.params['sensors']['baselineEco2']), int(self.config.params['sensors']['baselineTvoc'])])
        self.openWeather = OpenWeatherMap(apiKey=self.config.params['api']['openWeatherApi'],
                                          latitude=self.config.params['location']['latitude'],
                                          longitude=self.config.params['location']['longitude'])

    def reloadConfig(self):
        self.sgp.resetDevice()
        self.sgp.initConfig([int(self.config.params['sensors']['baselineEco2']), int(self.config.params['sensors']['baselineTvoc'])])
        self.openWeather.setLocation(latitude=self.config.params['location']['latitude'],
                                          longitude=self.config.params['location']['longitude'])
        self.updateWeatherReport()

    def updateWeatherReport(self):
        self.weatherReport = self.openWeather.getReport()
        if (self.weatherReport != None):
            print('[WeatherStation] Report Update:')
            print(prettyJson(
                {
                    'location' : self.config.params['location']['city'],
                    'temperature' : str(self.weatherReport['current']['temp']) + 'C',
                    'pressure' : str(self.weatherReport['current']['pressure']) + 'mbar',
                    'humidity' : str(self.weatherReport['current']['humidity']) + '%',
                    'weather' : self.weatherReport['current']['weather'][0]['description']
                }
            ))
        else:
            print('[WeatherStation] Error updating report.')


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
        if(self.weatherReport != None):
            myMeas = Measurement(
            datetime=datetime.now(),
            cityMeas=CityMeas(
                location=self.config.params['location']['city'],
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
        else:
            print('[WeatherStation] Error inserting data to DB.')

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

        try:
            return dictionary[self.weatherReport['current']['weather'][0]['icon']]
        except:
            return 0
