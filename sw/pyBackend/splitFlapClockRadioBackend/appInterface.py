from splitFlapClockRadioBackend.audio.audio import Audio
from splitFlapClockRadioBackend.clock.clockThread import ClockThread
from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.mainControl import MainControlThread
from splitFlapClockRadioBackend.osInfo.osInfoThread import osInfoThread
from splitFlapClockRadioBackend.radioTuner.radioTunerThread import RadioTunerThread
from splitFlapClockRadioBackend.rgbStrip.rgbStripThread import RgbStripThread
from splitFlapClockRadioBackend.spotifyPlayer.spotifyPlayer import SpotifyPlayer
from splitFlapClockRadioBackend.userInterface.userInterface import UserInterface
from splitFlapClockRadioBackend.weatherStation.weatherStationThread import WeatherStationThread
from splitFlapClockRadioBackend.webServer.webServer import webServerThread


class App:
    config: Config = None
    dbCtl: dbController = None
    userInterface: UserInterface = None
    audio: Audio = None
    spotifyPlayer: SpotifyPlayer = None
    osInfoTh: osInfoThread = None
    weatherStationTh: WeatherStationThread = None
    lightStripTh: RgbStripThread = None
    radioTunerTh: RadioTunerThread = None
    clockTh: ClockThread = None
    mainControlTh: MainControlThread = None
    webserverTh: webServerThread = None
