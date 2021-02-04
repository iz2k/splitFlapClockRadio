import time
from datetime import timedelta, datetime
from queue import Queue
from threading import Thread

from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getNow


from splitFlapClockRadioBackend.weatherStation.bme680.simpleBme680 import SimpleBME680
from splitFlapClockRadioBackend.weatherStation.sgp30.simpleSgp30 import SimpleSGP30
from splitFlapClockRadioBackend.weatherStation.openWeatherMap.openWeatherMap import OpenWeatherMap
from splitFlapClockRadioBackend.dbManager import Measurement, CityMeas, HomeMeas


class WeatherStation(Thread):

    queue = Queue()

    weatherReport = {}
    sensorReport = {}
    todayForecast = ''

    bme = None
    sgp = None
    openWeather = None


    def __init__(self, app):
        Thread.__init__(self)
        from splitFlapClockRadioBackend.__main__ import App
        self.app: App = app
        self.bme = SimpleBME680()
        self.sgp = SimpleSGP30([int(self.app.config.params['sensors']['baselineEco2']), int(self.app.config.params['sensors']['baselineTvoc'])])
        self.openWeather = OpenWeatherMap(apiKey=self.app.config.params['api']['openWeatherApi'],
                                          latitude=self.app.config.params['location']['latitude'],
                                          longitude=self.app.config.params['location']['longitude'])

        from splitFlapClockRadioBackend.weatherStation.weatherStationWebRoutes import defineWeatherStationWebRoutes
        defineWeatherStationWebRoutes(self.app)

        self.start()

    def start(self):
        Thread.start(self)

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('WeatherStation thread exit.')


    def run(self):

        interval_minutes = 10

        last_update = getNow() - timedelta(minutes=interval_minutes)

        # Main loop
        run_app=True
        while(run_app):
            # Check if msg in queue
            while not self.queue.empty():
                [q_msg, q_data] = self.queue.get()
                if q_msg == 'quit':
                    run_app=False

            self.updateSensorReport()
            if ('humidity' in self.sensorReport):
                self.sgp.adjustRH(self.sensorReport['humidity'])
            self.emit()

            now = getNow()
            next_update = last_update + timedelta(minutes=interval_minutes)
            if now > next_update:
                last_update = now
                self.updateWeatherReport()
                self.app.webserver.sio.emit('weatherReport', self.weatherReport)
                self.insertToDb()
                self.app.clock.update_weather(self.get_ww_idx())

            time.sleep(1)

    def emit(self):
        self.app.webserver.sio.emit('sensorData', prettyJson(self.sensorReport))


    def reloadSensors(self):
        self.sgp.resetDevice()
        self.sgp.initConfig([int(self.app.config.params['sensors']['baselineEco2']), int(self.app.config.params['sensors']['baselineTvoc'])])

    def reloadWeather(self):
        print('reloadWeather')
        self.openWeather.setApiKey(apiKey=self.app.config.params['api']['openWeatherApi'])
        self.openWeather.setLocation(latitude=self.app.config.params['location']['latitude'],
                                     longitude=self.app.config.params['location']['longitude'])
        self.updateWeatherReport()

    def updateWeatherReport(self):
        self.weatherReport = self.openWeather.getReport()
        if (self.weatherReport != None):
            print('[weather] Updating Weather Report')
            self.updateTodayForecast()
        else:
            print('[weather] Error updating Weather Report.')

    def updateTodayForecast(self):
        fc = 'Actualmente, hace una temperatura de ' + str(round(self.weatherReport['current']['temp'])) + ' grados'
        fc = fc + ' y ' + str(self.weatherReport['current']['weather'][0]['description']) + '.'
        fc = fc + ' A lo largo del día se espera ' + str(self.weatherReport['daily'][0]['weather'][0]['description'])
        fc = fc + ' con temperaturas entre los ' + str(round(self.weatherReport['daily'][0]['temp']['min'])) +\
             ' y ' + str(round(self.weatherReport['daily'][0]['temp']['max'])) + ' grados.'
        fc = fc + ' La probabilidad de que hoy llueva es del ' + str(round(self.weatherReport['daily'][0]['pop']*100)) + '%'

        self.todayForecast = fc

    def updateSensorReport(self):
        bmedata = self.bme.getSensorData()
        for parameter in bmedata:
            self.sensorReport[parameter] = bmedata[parameter]
        sgpdata = self.sgp.getSensorData()
        for parameter in sgpdata:
            self.sensorReport[parameter] = sgpdata[parameter]

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
            print('[weather] Error inserting data to DB.')

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
