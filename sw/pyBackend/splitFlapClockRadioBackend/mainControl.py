from datetime import datetime, timedelta
import time
from queue import Queue
from threading import Thread

from flask_socketio import SocketIO

from splitFlapClockRadioBackend.audio.audio import Audio
from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.rgbStrip.rgbStripThread import RgbStripThread


class MainControlThread(Thread):

    queue = Queue()

    dbCtl : dbController = None
    audio : Audio = None
    lightStripTh : RgbStripThread= None
    sio : SocketIO = None

    def __init__(self, dbCtl, audio, lightStripTh):
        Thread.__init__(self)
        self.dbCtl = dbCtl
        self.audio = audio
        self.lightStripTh = lightStripTh

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
                    self.audio.say_text('Iniciando reloj.', lang='es')
                    self.lightStripTh.test()
                if q_msg == 'volume_rotary':
                    if self.queue.empty():
                        print("[MAIN] VOL_ROTARY " + str(q_data))
                        if q_data == 1:
                            self.audio.volume_up()
                        if q_data == -1:
                            self.audio.volume_down()
                        self.lightStripTh.vol_update(self.audio.volume)
                if q_msg == 'volume_switch':
                    print("[MAIN] VOL_SWITCH " + str(q_data))
                    if q_data == 'short':
                        pass
                    if q_data == 'long':
                        pass
                if q_msg == 'control_rotary':
                    print("[MAIN] CTL_ROTARY " + str(q_data))
                    if q_data == 1:
                        self.audio.volume_up()
                    if q_data == -1:
                        self.audio.volume_down()
                if q_msg == 'control_switch':
                    print("[MAIN] CTL_SWITCH " + str(q_data))
                    if q_data == 'short':
                        pass
                    if q_data == 'long':
                        pass

            time.sleep(0.1)
