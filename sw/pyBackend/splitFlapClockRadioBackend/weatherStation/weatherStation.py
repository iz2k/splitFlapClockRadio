from datetime import datetime

from splitFlapClockRadioBackend.weatherStation.bme680.simpleBme680 import SimpleBME680
from splitFlapClockRadioBackend.weatherStation.sgp30.simpleSgp30 import SimpleSGP30
from splitFlapClockRadioBackend.weatherStation.openWeatherMap.openWeatherMap import OpenWeatherMap
from splitFlapClockRadioBackend.dbManager import Measurement, CityMeas, HomeMeas
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


class WeatherStation:

    weatherReport = {}
    sensorReport = {}
    todayForecast = ''

    bme = None
    sgp = None
    openWeather = None


    def __init__(self, app):
        from splitFlapClockRadioBackend.appInterface import App
        self.app: App = app
        self.bme = SimpleBME680()
        self.sgp = SimpleSGP30([int(self.app.config.params['sensors']['baselineEco2']), int(self.app.config.params['sensors']['baselineTvoc'])])
        self.openWeather = OpenWeatherMap(apiKey=self.app.config.params['api']['openWeatherApi'],
                                          latitude=self.app.config.params['location']['latitude'],
                                          longitude=self.app.config.params['location']['longitude'])

    def reloadSensors(self):
        self.sgp.resetDevice()
        self.sgp.initConfig([int(self.app.config.params['sensors']['baselineEco2']), int(self.app.config.params['sensors']['baselineTvoc'])])

    def reloadWeather(self):
        self.openWeather.setLocation(latitude=self.app.config.params['location']['latitude'],
                                     longitude=self.app.config.params['location']['longitude'])
        self.updateWeatherReport()

    def updateWeatherReport(self):
        self.weatherReport = self.openWeather.getReport()
        if (self.weatherReport != None):
            print('[weather] Report Update:')
            print(prettyJson(
                {
                    'location' : self.app.config.params['location']['city'],
                    'temperature' : str(self.weatherReport['current']['temp']) + 'C',
                    'pressure' : str(self.weatherReport['current']['pressure']) + 'mbar',
                    'humidity' : str(self.weatherReport['current']['humidity']) + '%',
                    'weather' : self.weatherReport['current']['weather'][0]['description']
                }
            ))
            self.updateTodayForecast()
        else:
            print('[weather] Error updating report.')

    def updateTodayForecast(self):
        fc = 'Actualmente, hace una temperatura de ' + str(round(self.weatherReport['current']['temp'])) + ' grados'
        fc = fc + ' y ' + str(self.weatherReport['current']['weather'][0]['description']) + '.'
        fc = fc + ' A lo largo del día se espera ' + str(self.weatherReport['daily'][0]['weather'][0]['description'])
        fc = fc + ' con temperaturas entre los ' + str(round(self.weatherReport['daily'][0]['temp']['min'])) +\
             ' y ' + str(round(self.weatherReport['daily'][0]['temp']['max'])) + ' grados.'
        fc = fc + ' La probabilidad de que hoy llueva es del ' + str(round(self.weatherReport['daily'][0]['pop']*100)) + '%'

        self.todayForecast = fc

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
                location=self.app.config.params['location']['city'],
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

            self.app.dbCtl.insert(myMeas)
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
