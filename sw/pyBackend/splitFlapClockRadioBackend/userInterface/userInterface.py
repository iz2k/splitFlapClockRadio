import time
from queue import Queue
from threading import Thread

from splitFlapClockRadioBackend.userInterface.rotary import rotary
from splitFlapClockRadioBackend.userInterface.switch import switch


class UserInterface(Thread):

    queue = Queue()

    def __init__(self, app):
        Thread.__init__(self)
        from splitFlapClockRadioBackend.__main__ import App
        self.app: App = app
        # Create VOL rotary
        vol_rotary = rotary(A=24, B=25, callback=self.vol_rotary_callback)

        # Create VOL switch
        vol_switch = switch(I=23)
        vol_switch.setup_switch(long_press=True, sw_short_callback=self.vol_sw_short, sw_long_callback=self.vol_sw_long)

        # Create CTRL rotary
        ctl_rotary = rotary(A=27, B=22, callback=self.ctrl_rotary_callback)

        # Create CTRL switch
        ctrl_switch = switch(I=9)
        ctrl_switch.setup_switch(long_press=True, sw_short_callback=self.ctrl_sw_short, sw_long_callback=self.ctrl_sw_long)

        self.start()

    def start(self):
        Thread.start(self)
        self.queue.put(['startup', 0])

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('thread exit cleanly')

    def vol_rotary_callback(self, direction):
        print("[ui] VOL_ROTARY:", direction)
        self.queue.put(['volume_rotary', direction])

    def vol_sw_short(self):
        print("[ui] VOL_SW SHORT")
        self.queue.put(['volume_switch', 'short'])

    def vol_sw_long(self):
        print("[ui] VOL_SW LONG")
        self.queue.put(['volume_switch', 'long'])

    def ctrl_rotary_callback(self, direction):
        print("[ui] CTRL_ROTARY:", direction)
        self.queue.put(['control_rotary', direction])

    def ctrl_sw_short(self):
        print("[ui] CTRL_SW SHORT")
        self.queue.put(['control_switch', 'short'])

    def ctrl_sw_long(self):
        print("[ui] CTRL_SW LONG")
        self.queue.put(['control_switch', 'long'])

    def run(self):
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
        self.app.lightStrip.test()

    def changeVolume(self, action):
        if (self.app.audio.mute == True):
            self.toggleMute()
        if action == 1:
            self.app.audio.volume_up()
        if action == -1:
            self.app.audio.volume_down()
        self.app.lightStrip.vol_update(self.app.audio.volume)

    def toggleMute(self):
        self.app.audio.toggle_mute()
        self.app.lightStrip.vol_toggleMute(self.app.audio.mute)

    def changeMediaSource(self):
        if self.app.radioTuner.radioTuner.on:
            self.app.audio.play('on')
            self.app.radioTuner.pause()
            self.app.spotifyPlayer.play('spotify:playlist:2z7k6r8z0OlXuDsIuy80ZN')
        elif self.app.spotifyPlayer.isOn:
            self.app.audio.play('off')
            self.app.spotifyPlayer.pause()
        else:
            self.app.audio.play('on')
            self.app.radioTuner.tune(97.2)
            self.app.radioTuner.play()


    def changeMediaItem(self, action):

        if self.app.radioTuner.radioTuner.on:
            self.app.audio.play('source')
            if action == 1:
                self.app.radioTuner.next()
            elif action == -1:
                self.app.radioTuner.previous()
        elif self.app.spotifyPlayer.isOn:
            self.app.audio.play('source')
            if action == 1:
                self.app.spotifyPlayer.next()
            elif action == -1:
                self.app.spotifyPlayer.previous()
