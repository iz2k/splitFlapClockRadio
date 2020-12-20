#!/usr/bin/env python3
import argparse
import time

from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.osInfo.osInfoThread import osInfoThread
from splitFlapClockRadioBackend.userInterface.rotary import rotary
from splitFlapClockRadioBackend.userInterface.switch import switch
from splitFlapClockRadioBackend.userInterface.userInterface import UserInterface
from splitFlapClockRadioBackend.weatherStation.weatherStationThread import WeatherStationThread
from splitFlapClockRadioBackend.webServer.webServer import webServerThread
from splitFlapClockRadioBackend.rgbStrip.rgbStripThread import RgbStripThread


def vol_rotary_callback(direction):
    print("[UI] VOL_ROTARY:", direction)


def vol_sw_short():
    print("[UI] VOL_SW SHORT")


def vol_sw_long():
    print("[UI] VOL_SW LONG")

def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description="iz2k's split-clock controller.")

    parser.add_argument("-port", default='8081', help=" port used for web server")

    args = parser.parse_args()

    #dbCtl = dbController()
    userInterface = UserInterface()

    while True:
        time.sleep(1)

    # Define threads
    webserverTh = webServerThread(log=False)
    osInfoTh = osInfoThread()
    weatherStationTh = WeatherStationThread(dbCtl=dbCtl)
    lightStripTh = RgbStripThread()

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
        webserverTh.start(port=args.port, host='0.0.0.0', debug=False, use_reloader=False)

        # Testing
        lightStripTh.queue.put(['test', 0])

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
