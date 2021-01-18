import time
from datetime import timedelta
from queue import Queue
from threading import Thread

from flask_socketio import SocketIO

from splitFlapClockRadioBackend.radioTuner.si4731 import Si4731
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.osTools import start_service
from splitFlapClockRadioBackend.tools.timeTools import getNow


class RadioTunerThread(Thread):

    queue = Queue()
    radioTuner = None

    def __init__(self):
        Thread.__init__(self)
        self.radioTuner = Si4731()
        start_service('i2s-pipe')

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

        interval_seconds = 0.5

        last_update = getNow() - timedelta(seconds=interval_seconds)
        # Main loop
        run_app=True
        while(run_app):

            # Update Radio Signal Quality
            self.radioTuner.get_rsq_status()

            # Check if RDS data vailable
            if (self.radioTuner.check_rds()):
                # Get and Process RDS data
                self.radioTuner.get_rds_status()

            # Check if msg in queue
            while not self.queue.empty():
                [q_msg, q_data] = self.queue.get()
                if q_msg == 'quit':
                    run_app=False
                if (q_msg == 'tune'):
                    self.radioTuner.fm_tune(q_data)
                if (q_msg == 'turn_on'):
                    self.radioTuner.turn(True)
                if (q_msg == 'turn_off'):
                    self.radioTuner.turn(False)
                if (q_msg == 'seek_up'):
                    self.radioTuner.fm_seek_up()
                if (q_msg == 'seek_down'):
                    self.radioTuner.fm_seek_down()

            now = getNow()
            next_update = last_update + timedelta(seconds=interval_seconds)
            if now > next_update:
                last_update = now
                self.emitFmRadioReport()
            time.sleep(0.1)


    def tune(self, freq):
        self.queue.put(['tune', freq])
        print('[radio] TUNE ' + str(freq) + 'MHz')

    def play(self):
        self.queue.put(['turn_on', 0])
        print('[radio] PLAY')

    def pause(self):
        self.queue.put(['turn_off', 0])
        print('[radio] PAUSE')


    def next(self):
        self.queue.put(['seek_up', 0])
        print('[radio] SEEK UP')


    def previous(self):
        self.queue.put(['seek_down', 0])
        print('[radio] SEEK DOWN')

    def emitFmRadioReport(self):
        self.sio.emit('fmRadioReport', prettyJson(self.radioTuner.get_info_obj()))
