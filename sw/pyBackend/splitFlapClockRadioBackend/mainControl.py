import time
from queue import Queue
from threading import Thread


class MainControlThread(Thread):

    queue = Queue()

    def __init__(self, app):
        Thread.__init__(self)
        from splitFlapClockRadioBackend.appInterface import App
        self.app: App = app

    def start(self):
        Thread.start(self)
        self.queue.put(['startup', 0])

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('thread exit cleanly')

    def run(self):

        # TODO: REMOVE. Just to autostart radio during development.
        #self.changeMediaSource()
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

            time.sleep(0.1)

    def systemStartup(self):
        self.app.audio.say_text_offline('Iniciando reloj.', lang='es-ES')
        self.app.lightStripTh.test()

    def changeVolume(self, action):
        if (self.app.audio.mute == True):
            self.toggleMute()
        if action == 1:
            self.app.audio.volume_up()
        if action == -1:
            self.app.audio.volume_down()
        self.app.lightStripTh.vol_update(self.app.audio.volume)

    def toggleMute(self):
        self.app.audio.toggle_mute()
        self.app.lightStripTh.vol_toggleMute(self.app.audio.mute)

    def changeMediaSource(self):
        if self.app.radioTunerTh.radioTuner.on:
            self.app.audio.play('on')
            self.app.radioTunerTh.pause()
            self.app.spotifyPlayer.play('spotify:playlist:2z7k6r8z0OlXuDsIuy80ZN')
        elif self.app.spotifyPlayer.isOn:
            self.app.audio.play('off')
            self.app.spotifyPlayer.pause()
        else:
            self.app.audio.play('on')
            self.app.radioTunerTh.tune(97.2)
            self.app.radioTunerTh.play()


    def changeMediaItem(self, action):

        if self.app.radioTunerTh.radioTuner.on:
            self.app.audio.play('source')
            if action == 1:
                self.app.radioTunerTh.next()
            elif action == -1:
                self.app.radioTunerTh.previous()
        elif self.app.spotifyPlayer.isOn:
            self.app.audio.play('source')
            if action == 1:
                self.app.spotifyPlayer.next()
            elif action == -1:
                self.app.spotifyPlayer.previous()
