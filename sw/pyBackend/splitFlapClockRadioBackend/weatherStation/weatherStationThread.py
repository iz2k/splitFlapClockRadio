import time
from datetime import timedelta
from queue import Queue
from threading import Thread

from flask_socketio import SocketIO

from splitFlapClockRadioBackend.clock.clockThread import ClockThread
from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getNow
from splitFlapClockRadioBackend.weatherStation.weatherStation import WeatherStation


class WeatherStationThread(Thread):

    queue = Queue()
    weatherStation = None
    clockTh = None

    def __init__(self, dbCtl : dbController, config):
        Thread.__init__(self)
        self.weatherStation = WeatherStation(dbCtl, config)

    def start(self):
        Thread.start(self)

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('thread exit cleanly')

    def set_sio(self, sio : SocketIO):
        self.sio = sio

    def set_clockTh(self, clockTh: ClockThread):
        self.clockTh = clockTh

    def run(self):

        interval_minutes = 5

        last_update = getNow() - timedelta(minutes=interval_minutes)

        # Main loop
        run_app=True
        while(run_app):
            # Check if msg in queue
            while not self.queue.empty():
                [q_msg, q_data] = self.queue.get()
                if q_msg == 'quit':
                    run_app=False

            self.weatherStation.updateSensorReport()
            self.weatherStation.sgp.adjustRH(self.weatherStation.sensorReport['humidity'])
            #self.emit()

            now = getNow()
            next_update = last_update + timedelta(minutes=interval_minutes)
            if now > next_update:
                last_update = now
                self.weatherStation.updateWeatherReport()
                self.weatherStation.insertToDb()
                self.clockTh.update_weather(self.weatherStation.get_ww_idx())

            time.sleep(1)

    def emit(self):
        self.sio.emit('sensorData', prettyJson(self.weatherStation.sensorReport))
