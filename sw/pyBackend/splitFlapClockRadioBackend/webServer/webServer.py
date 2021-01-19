from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from queue import Queue
from threading import Thread

from splitFlapClockRadioBackend.clock.clockThread import ClockThread
from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.radioTuner.radioTunerThread import RadioTunerThread
from splitFlapClockRadioBackend.spotifyPlayer.spotifyPlayer import SpotifyPlayer
from splitFlapClockRadioBackend.tools.ipTools import getHostname, getIP
from splitFlapClockRadioBackend.weatherStation.weatherStation import WeatherStation
from splitFlapClockRadioBackend.webServer.routesClock import defineClockRoutes
from splitFlapClockRadioBackend.webServer.routesConfig import defineConfigRoutes
from splitFlapClockRadioBackend.webServer.routesDataBase import defineDataBaseRoutes
from splitFlapClockRadioBackend.webServer.routesInfo import defineInfoRoutes
from splitFlapClockRadioBackend.webServer.routesRadioTuner import defineRadioTunerRoutes
from splitFlapClockRadioBackend.webServer.routesSpotify import defineSpotifyRoutes
from splitFlapClockRadioBackend.webServer.routesWeatherStation import defineWeatherStationRoutes


class webServerThread(Thread):

    queue = Queue()
    sio : SocketIO = None
    flaskApp : Flask = None

    def __init__(self, log):
        Thread.__init__(self)

        # Create Flask App
        self.flaskApp = Flask(__name__, static_folder='web', static_url_path='')
        # Enable CORS to Flask
        CORS(self.flaskApp)
        # Add SocketIO to app
        self.sio = SocketIO(self.flaskApp, cors_allowed_origins="*", logger=log, engineio_logger=log, async_mode='threading')

    def start(self, port, host, debug, use_reloader):
        self.port = port
        self.host = host
        self.debug = debug
        self.use_reloader = use_reloader
        Thread.start(self)

    def stop(self):
        print('trying to stop flask')

    def run(self):
        # When server starts, set flag
        self.isRunning = True

        # Start Webserver (blocks this thread until server quits)
        print('Starting Web Server:')
        print('\t\thttp://' + getHostname() + ':' + str(self.port))
        print('\t\thttp://' + getIP() + ':' + str(self.port))
        self.sio.run(self.flaskApp, port=self.port, host=self.host, debug=self.debug, use_reloader = self.use_reloader)

        # When server ends, reset flag
        self.isRunning = False

    def define_webroutes(self, weather : WeatherStation, dbCtl : dbController, config : Config, clockTh : ClockThread, radioTunerTh : RadioTunerThread, spotifyPl : SpotifyPlayer):
        defineInfoRoutes(self.sio)
        defineConfigRoutes(self.flaskApp, config)
        defineWeatherStationRoutes(self.flaskApp, weather)
        defineDataBaseRoutes(self.flaskApp, dbCtl)
        defineClockRoutes(self.flaskApp, config, clockTh)
        defineRadioTunerRoutes(self.flaskApp, self.sio, config, radioTunerTh)
        defineSpotifyRoutes(self.flaskApp, self.sio, config, spotifyPl)
