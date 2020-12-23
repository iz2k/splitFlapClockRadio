from datetime import datetime, timedelta
import time
from queue import Queue
from threading import Thread

from flask_socketio import SocketIO

from splitFlapClockRadioBackend.audio.audio import Audio
from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.rgbStrip.rgbStripThread import RgbStripThread
from splitFlapClockRadioBackend.spotifyPlayer.spotifyPlayer import SpotifyPlayer


class MainControlThread(Thread):

    queue = Queue()

    dbCtl : dbController = None
    audio : Audio = None
    lightStripTh : RgbStripThread= None
    sio : SocketIO = None
    spotifyPlayer : SpotifyPlayer = None

    def __init__(self, dbCtl, audio, lightStripTh, spotifyPlayer):
        Thread.__init__(self)
        self.dbCtl = dbCtl
        self.audio = audio
        self.lightStripTh = lightStripTh
        self.spotifyPlayer = spotifyPlayer

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
                    #self.audio.say_text('Iniciando reloj.', lang='es')
                    self.lightStripTh.test()
                if q_msg == 'volume_rotary':
                    if self.queue.empty():
                        if q_data == 1:
                            self.audio.volume_up()
                        if q_data == -1:
                            self.audio.volume_down()
                        self.lightStripTh.vol_update(self.audio.volume)
                if q_msg == 'volume_switch':
                    if q_data == 'short':
                        pass
                    if q_data == 'long':
                        pass
                if q_msg == 'control_rotary':
                    self.audio.play('beep')
                    if q_data == 1:
                        self.spotifyPlayer.next()
                    if q_data == -1:
                        self.spotifyPlayer.previous()
                if q_msg == 'control_switch':
                    if q_data == 'short':
                        self.spotifyPlayer.play()
                    if q_data == 'long':
                        self.spotifyPlayer.pause()

            time.sleep(0.1)
