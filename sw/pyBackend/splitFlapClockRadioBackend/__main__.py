#!/usr/bin/env python3
import argparse

from splitFlapClockRadioBackend.alarm.alarm import Alarm
from splitFlapClockRadioBackend.audio.audio import Audio
from splitFlapClockRadioBackend.clock.clock import Clock
from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.osInfo.osInfo import osInfo
from splitFlapClockRadioBackend.radioTuner.radioTuner import RadioTuner
from splitFlapClockRadioBackend.spotifyPlayer.spotifyPlayer import SpotifyPlayer
from splitFlapClockRadioBackend.userInterface.userInterface import UserInterface
from splitFlapClockRadioBackend.weatherStation.weatherStation import WeatherStation
from splitFlapClockRadioBackend.webServer.WebServer import WebServer
from splitFlapClockRadioBackend.rgbStrip.rgbStrip import RgbStrip

class App:
    webserver: WebServer = None
    config: Config = None
    audio: Audio = None
    lightStrip: RgbStrip = None
    dbCtl: dbController = None
    osInfo: osInfo = None
    clock: Clock = None
    alarm: Alarm = None
    radioTuner: RadioTuner = None
    spotifyPlayer: SpotifyPlayer = None
    weatherStation: WeatherStation = None
    userInterface: UserInterface = None

def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description="iz2k's split-flap-clock controller.")
    parser.add_argument("-port", default='80', help=" port used for web server")
    parser.add_argument("-frontend", default='/usr/share/iz2k/splitFlapClockRadioFrontend/public', help=" path to FrontEnd")
    args = parser.parse_args()

    app = App()
    app.webserver = WebServer(app=app, staticPath=args.frontend)
    app.config = Config(app=app)
    app.audio = Audio(app=app)
    app.lightStrip = RgbStrip(app=app)
    app.dbCtl = dbController(app=app)
    app.osInfo = osInfo(app=app)
    app.clock = Clock(app=app)
    app.alarm = Alarm(app=app)
    app.radioTuner = RadioTuner(app=app)
    app.spotifyPlayer = SpotifyPlayer(app=app)
    app.weatherStation = WeatherStation(app=app)
    app.userInterface = UserInterface(app=app)


    try:
        # Start Web Server
        app.webserver.start(port=args.port, host='0.0.0.0', debug=False, use_reloader=False)

        # Wait while server running
        app.webserver.join()
        print('WebServer thread exit.')

        # When server ends, stop threads
        stopThreads(app)

    except KeyboardInterrupt:
        stopThreads(app)

def stopThreads(app: App):
    print('Ending application by user request.')
    app.clock.stop()
    app.alarm.stop()
    app.osInfo.stop()
    app.weatherStation.stop()
    app.lightStrip.stop()
    app.radioTuner.stop()
    app.userInterface.stop()
    print('Application ended.')


# If executed as main, call main
if __name__ == "__main__":
    main()
