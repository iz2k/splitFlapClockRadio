import time
from datetime import timedelta
from queue import Queue
from threading import Thread

from splitFlapClockRadioBackend.radioTuner.si4731 import Si4731
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.osTools import start_service
from splitFlapClockRadioBackend.tools.timeTools import getNow


class RadioTuner(Thread):

    queue = Queue()
    radioTuner = None
    lastReport = None
    freq = None

    def __init__(self, app):
        Thread.__init__(self)
        from splitFlapClockRadioBackend.__main__ import App
        self.app: App = app
        self.radioTuner = Si4731()
        start_service('i2s-pipe')
        self.lastReport = self.radioTuner.get_info_obj()

        from splitFlapClockRadioBackend.radioTuner.radioTunerWebRoutes import defineRadioTunerWebRoutes
        defineRadioTunerWebRoutes(self.app)

        self.start()

    def start(self):
        Thread.start(self)

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('RadioTuner thread exit.')

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
                if (q_msg == 'reset'):
                    self.radioTuner.__init__()
                    if self.freq != None:
                        self.radioTuner.fm_tune(self.freq)
                if (q_msg == 'tune'):
                    self.radioTuner.fm_tune(q_data)
                if (q_msg == 'turn_on'):
                    self.radioTuner.turn(True)
                if (q_msg == 'turn_off'):
                    self.radioTuner.turn(False)
                    self.emitFmRadioReport()
                if (q_msg == 'seek_up'):
                    self.radioTuner.fm_seek_up()
                if (q_msg == 'seek_down'):
                    self.radioTuner.fm_seek_down()

            if self.detectFmRadioReportChange():
                if self.radioTuner.on:
                    self.emitFmRadioReport()

            time.sleep(0.1)


    def tune(self, freq):
        self.freq = freq
        self.queue.put(['tune', self.freq])
        print('[radio] TUNE ' + str(self.freq) + 'MHz')

    def play(self):
        self.queue.put(['reset', 0])
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

    def detectFmRadioReportChange(self):
        newReport = self.radioTuner.get_info_obj()
        hasChanged = False
        for key in self.lastReport:
            if (self.lastReport[key] != newReport[key]):
                hasChanged = True
        self.lastReport = newReport
        return hasChanged

    def emitFmRadioReport(self):
        self.app.webserver.sio.emit('fmRadioReport', prettyJson(self.radioTuner.get_info_obj()))
