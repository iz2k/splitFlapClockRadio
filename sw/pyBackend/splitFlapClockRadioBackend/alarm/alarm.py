import copy
import time
from datetime import timedelta
from queue import Queue
from threading import Thread

from splitFlapClockRadioBackend.tools.timeTools import getTimeZoneAwareNow


class Alarm(Thread):

    queue = Queue()
    alarms = None

    def __init__(self, app):
        Thread.__init__(self)
        from splitFlapClockRadioBackend.__main__ import App
        self.app: App = app

        self.loadAlarms()

        from splitFlapClockRadioBackend.alarm.alarmWebRoutes import defineAlarmWebRoutes
        defineAlarmWebRoutes(self.app)

        self.start()

    def start(self):
        Thread.start(self)

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('Alarm thread exit.')

    def loadAlarms(self):
        self.alarms = copy.deepcopy(self.app.config.params['clock']['alarms'])
        for alarm in self.alarms:
            alarm['status'] = 'off'
            alarm['lastOffDate'] = getTimeZoneAwareNow(self.app.config.params['clock']['timeZone']) - timedelta(days=1)

    def run(self):
        # Main loop
        run_app=True
        while(run_app):

            # Check if msg in queue
            while not self.queue.empty():
                [q_msg, q_data] = self.queue.get()
                if q_msg == 'quit':
                    run_app=False

            # Keep track of time
            curTime = getTimeZoneAwareNow(self.app.config.params['clock']['timeZone'])
            for alarm in self.alarms:
                if (alarm['Active'] == True):
                # Alarm is active
                    if (alarm['WeekDays'][curTime.weekday()] == True):
                    # WeekDay matches
                        if (alarm['lastOffDate'] < getTimeZoneAwareNow(self.app.config.params['clock']['timeZone']) - timedelta(days=1)):
                        # Alarm has not been switched off today
                            if (alarm['status'] == 'off'):
                                if (alarm['Hour'] == curTime.hour and alarm['Minute'] == curTime.minute):
                                # Hour&Minute matches
                                    self.triggerAlarm(alarm)
                            if (alarm['status'] == 'snooze'):
                                # TODO: Snooze functionality
                                self.triggerAlarm(alarm)

            time.sleep(0.1)

    def triggerAlarm(self, alarm):
        print('[alarm] Triggering alarm >> ' + alarm['Name'] + ' <<')
        alarm['status'] = 'on'
        self.app.lightStrip.test()
        textToSpeak = ''
        if (alarm['Message'] != ''):
            textToSpeak = textToSpeak + alarm['Message'] + '. '
        if (alarm['EnableWeatherForecast'] == True):
            textToSpeak = textToSpeak + self.app.weatherStation.todayForecast + '. '
        if textToSpeak != '':
            self.app.audio.say_text_offline(textToSpeak, lang='es-ES', wait=True)
        if (alarm['PlaySource'] == 'Spotify'):
            self.app.spotifyPlayer.play(alarm['PlayItem']['URI'])
        if (alarm['PlaySource'] == 'Radio'):
            self.app.radioTuner.tune(alarm['PlayItem']['Frequency'])
            self.app.radioTuner.play()

    def stopActiveAlarms(self):
        stopped = False
        for alarm in self.alarms:
            if (alarm['status'] == 'on' or alarm['status'] == 'snooze'):
                print('[alarm] Stopping alarm >> ' + alarm['Name'] + ' <<')
                alarm['status'] = 'off'
                alarm['lastOffDate'] = getTimeZoneAwareNow(self.app.config.params['clock']['timeZone'])
                stopped = True
        return stopped
