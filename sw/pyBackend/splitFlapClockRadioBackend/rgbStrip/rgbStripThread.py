import time
from datetime import timedelta
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
                if q_msg == 'quit':
                    run_app=False
                if q_msg == 'test':
                    self.rgbStrip.test()

            time.sleep(0.1)
