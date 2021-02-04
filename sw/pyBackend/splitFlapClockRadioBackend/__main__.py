#!/usr/bin/env python3
import argparse

from splitFlapClockRadioBackend.appInterface import App
from splitFlapClockRadioBackend.audio.audio import Audio
from splitFlapClockRadioBackend.clock.clockThread import ClockThread
from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.mainControl import MainControlThread
from splitFlapClockRadioBackend.osInfo.osInfoThread import osInfoThread
from splitFlapClockRadioBackend.radioTuner.radioTunerThread import RadioTunerThread
from splitFlapClockRadioBackend.spotifyPlayer.spotifyPlayer import SpotifyPlayer
from splitFlapClockRadioBackend.userInterface.userInterface import UserInterface
from splitFlapClockRadioBackend.weatherStation.weatherStationThread import WeatherStationThread
from splitFlapClockRadioBackend.webServer.webServer import webServerThread
from splitFlapClockRadioBackend.rgbStrip.rgbStripThread import RgbStripThread


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description="iz2k's split-flap-clock controller.")
    parser.add_argument("-port", default='8081', help=" port used for web server")
    args = parser.parse_args()

    app = App()
    app.config = Config(app=app)
    app.dbCtl = dbController(app=app)
    app.userInterface = UserInterface(app=app)
    app.audio = Audio(app=app)
    app.osInfoTh = osInfoThread(app=app)
    app.spotifyPlayer = SpotifyPlayer(app=app)

    app.weatherStationTh = WeatherStationThread(app=app)
    app.lightStripTh = RgbStripThread(app=app)
    app.radioTunerTh = RadioTunerThread(app=app)
    app.clockTh = ClockThread(app=app)
    app.mainControlTh = MainControlThread(app=app)

    app.webserverTh = webServerThread(app=app)
    app.webserverTh.define_webroutes()

    try:
        # Start threads
        app.osInfoTh.start()
        app.weatherStationTh.start()
        app.lightStripTh.start()
        app.radioTunerTh.start()
        app.clockTh.start()
        app.mainControlTh.start()
        app.webserverTh.start(port=args.port, host='0.0.0.0', debug=False, use_reloader=False)

        # Wait while server running
        app.webserverTh.join()

        # When server ends, stop threads
        app.osInfoTh.stop()
        app.weatherStationTh.stop()

        # Print Goodby msg
        print('Exiting...')

    except KeyboardInterrupt:
        # Stop threads
        app.osInfoTh.stop()
        app.weatherStationTh.stop()


# If executed as main, call main
if __name__ == "__main__":
    main()
