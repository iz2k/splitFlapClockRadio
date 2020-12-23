#!/usr/bin/env python3
import argparse

from splitFlapClockRadioBackend.audio.audio import Audio
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
    parser = argparse.ArgumentParser(description="iz2k's split-clock controller.")
    parser.add_argument("-port", default='8081', help=" port used for web server")
    args = parser.parse_args()

    dbCtl = dbController()
    userInterface = UserInterface()
    audio = Audio()
    spotifyPlayer = SpotifyPlayer()

    # Define threads
    osInfoTh = osInfoThread()
    weatherStationTh = WeatherStationThread(dbCtl=dbCtl)
    lightStripTh = RgbStripThread()
    radioTunerTh = RadioTunerThread()
    mainControlTh = MainControlThread(dbCtl=dbCtl, audio=audio, lightStripTh=lightStripTh, spotifyPlayer=spotifyPlayer, radioTunerTh=radioTunerTh)

    userInterface.set_mainControlQueue(mainControlTh.queue)

    webserverTh = webServerThread(log=False)
    webserverTh.define_webroutes(weather = weatherStationTh.weatherStation,
                                 dbCtl=dbCtl)

    # Pass SIO to threads
    osInfoTh.set_sio(webserverTh.sio)
    weatherStationTh.set_sio(webserverTh.sio)


    try:
        # Start threads
        osInfoTh.start()
        #weatherStationTh.start()
        lightStripTh.start()
        radioTunerTh.start()
        mainControlTh.start()
        webserverTh.start(port=args.port, host='0.0.0.0', debug=False, use_reloader=False)

        # Wait while server running
        webserverTh.join()

        # When server ends, stop threads
        osInfoTh.stop()
        weatherStationTh.stop()

        # Print Goodby msg
        print('Exiting R102-DB-CTL...')

    except KeyboardInterrupt:
        # Stop threads
        osInfoTh.stop()
        weatherStationTh.stop()


# If executed as main, call main
if __name__ == "__main__":
    main()
