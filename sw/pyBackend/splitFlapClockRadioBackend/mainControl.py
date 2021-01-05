import time
from queue import Queue
from threading import Thread
from pytz import timezone

from flask_socketio import SocketIO

from splitFlapClockRadioBackend.audio.audio import Audio
from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.radioTuner.radioTunerThread import RadioTunerThread
from splitFlapClockRadioBackend.rgbStrip.rgbStripThread import RgbStripThread
from splitFlapClockRadioBackend.splitFlap.splitFlapThread import SplitFlapThread
from splitFlapClockRadioBackend.spotifyPlayer.spotifyPlayer import SpotifyPlayer
from splitFlapClockRadioBackend.tools.timeTools import getTimeZoneAwareNow


class MainControlThread(Thread):

    queue = Queue()

    dbCtl : dbController = None
    audio : Audio = None
    lightStripTh : RgbStripThread= None
    sio : SocketIO = None
    spotifyPlayer : SpotifyPlayer = None
    radioTunerTh : RadioTunerThread = None
    splitFlapTh : SplitFlapThread = None

    mediaSource = 'None'

    def __init__(self, dbCtl, audio, lightStripTh, spotifyPlayer, radioTunerTh, splitFlapTh):
        Thread.__init__(self)
        self.dbCtl = dbCtl
        self.audio = audio
        self.lightStripTh = lightStripTh
        self.spotifyPlayer = spotifyPlayer
        self.radioTunerTh = radioTunerTh
        self.splitFlapTh = splitFlapTh

    def start(self):
        Thread.start(self)
        self.queue.put(['startup', 0])

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('thread exit cleanly')

    def set_sio(self, sio : SocketIO):
        self.sio = sio

    def run(self):
        # Main loop
        run_app=True
        while(run_app):
            # Check if msg in queue
            while not self.queue.empty():
                [q_msg, q_data] = self.queue.get()
                if q_msg == 'quit':
                    run_app=False
                if q_msg == 'startup':
                    self.systemStartup()
                if q_msg == 'volume_rotary':
                    if self.queue.empty():
                        self.changeVolume(q_data)
                if q_msg == 'volume_switch':
                    if q_data == 'short':
                        self.toggleMute()
                    if q_data == 'long':
                        pass
                if q_msg == 'control_rotary':
                    self.changeMediaItem(q_data)
                if q_msg == 'control_switch':
                    if q_data == 'short':
                        pass
                    if q_data == 'long':
                        self.changeMediaSource()

            self.updateTime()
            time.sleep(0.1)

    def updateTime(self):
        curTime = getTimeZoneAwareNow(timezone('Europe/Madrid'))
        self.splitFlapTh.update_time(curTime.hour, curTime.minute)

    def systemStartup(self):
        self.audio.say_text('Iniciando reloj.', lang='es')
        self.lightStripTh.test()

    def changeVolume(self, action):
        if (self.audio.mute == True):
            self.toggleMute()
        if action == 1:
            self.audio.volume_up()
        if action == -1:
            self.audio.volume_down()
        self.lightStripTh.vol_update(self.audio.volume)

    def toggleMute(self):
        self.audio.toggle_mute()
        self.lightStripTh.vol_toggleMute(self.audio.mute)

    def changeMediaSource(self):
        if self.mediaSource == 'None':
            self.audio.play('on')
            self.mediaSource = 'Radio'
            self.radioTunerTh.play(97.2)
        elif self.mediaSource == 'Radio':
            self.audio.play('on')
            self.radioTunerTh.stop()
            self.mediaSource = 'Spotify'
            self.spotifyPlayer.play('spotify:playlist:2z7k6r8z0OlXuDsIuy80ZN')
        elif self.mediaSource == 'Spotify':
            self.audio.play('off')
            self.spotifyPlayer.pause()
            self.mediaSource = 'None'

    def changeMediaItem(self, action):
        if self.mediaSource == 'None':
            pass
        elif self.mediaSource == 'Radio':
            self.audio.play('source')
            if action == 1:
                self.radioTunerTh.next()
            elif action == -1:
                self.radioTunerTh.previous()
        elif self.mediaSource == 'Spotify':
            self.audio.play('source')
            if action == 1:
                self.spotifyPlayer.next()
            elif action == -1:
                self.spotifyPlayer.previous()
