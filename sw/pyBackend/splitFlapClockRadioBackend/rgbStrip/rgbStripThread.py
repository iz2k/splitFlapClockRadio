import time
from datetime import timedelta, datetime
from queue import Queue
from threading import Thread

from flask_socketio import SocketIO

from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getNow
from splitFlapClockRadioBackend.rgbStrip.neoStrip import NeoStrip


class RgbStripThread(Thread):

    queue = Queue()
    rgbStrip = None
    signalingFlag : bool = False
    signalingExpire : time = None

    def __init__(self):
        Thread.__init__(self)
        self.rgbStrip = NeoStrip()

    def start(self):
        Thread.start(self)

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
                self.signalingFlag = True
                self.signalingExpire = datetime.now() + timedelta(seconds=1)
                if q_msg == 'quit':
                    run_app=False
                if q_msg == 'test':
                    self.rgbStrip.test()
                if q_msg == 'vol_update':
                    if self.queue.empty():
                        self.rgbStrip.vol_update(q_data)

            if self.signalingFlag == True and self.signalingExpire < datetime.now():
                self.signalingFlag = False
                self.rgbStrip.clear()

            time.sleep(0.1)

    def test(self):
        self.queue.put(['test', 0])

    def vol_update(self, volume):
        self.queue.put(['vol_update', volume])
