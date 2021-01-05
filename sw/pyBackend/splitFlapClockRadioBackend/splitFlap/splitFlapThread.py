import time
from queue import Queue
from threading import Thread

from flask_socketio import SocketIO

from splitFlapClockRadioBackend.splitFlap.smbusMsp430 import smbusMsp430


class SplitFlapThread(Thread):

    queue = Queue()
    smbusMsp430 = None
    desired_hh = None
    desired_mm = None
    desired_ww = None

    def __init__(self):
        Thread.__init__(self)
        self.smbus430 = smbusMsp430()
        time.sleep(1)
        self.desired_hh = self.smbus430.read_registerName('hh_desired_digit')
        self.desired_mm = self.smbus430.read_registerName('mm_desired_digit')
        self.desired_ww = self.smbus430.read_registerName('ww_desired_digit')

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
                if (q_msg == 'update_time'):
                    try:
                        self.smbus430.write_registerName('hh_desired_digit', q_data[0])
                        self.smbus430.write_registerName('mm_desired_digit', q_data[1])
                    except:
                        print('I2C error updating time')
                if (q_msg == 'update_weather'):
                    self.smbus430.write_registerName('ww_desired_digit', q_data)

            time.sleep(0.1)


    def update_time(self, hh, mm):
        if (hh != self.desired_hh or mm != self.desired_mm):
            self.queue.put(['update_time', [hh, mm]])
            self.desired_hh = hh
            self.desired_mm = mm
            print('[splitFlap] Update Time: ' + str(hh).zfill(2) + ':' + str(mm).zfill(2))

    def update_weather(self, ww):
        if (ww != self.desired_ww):
            self.queue.put(['update_time', ww])
            self.desired_ww = ww
            print('[splitFlap] Update Weather: ' + str(ww).zfill(2))

