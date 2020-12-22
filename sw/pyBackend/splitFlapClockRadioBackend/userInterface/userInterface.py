import time
from queue import Queue
from threading import Thread

from flask_socketio import SocketIO

from splitFlapClockRadioBackend.userInterface.rotary import rotary
from splitFlapClockRadioBackend.userInterface.switch import switch


class UserInterface:

    mainControlQueue = None

    def __init__(self):
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

    def set_sio(self, sio : SocketIO):
        self.sio = sio

    def set_mainControlQueue(self, mainControlQueue : Queue):
        self.mainControlQueue = mainControlQueue

    def vol_rotary_callback(self, direction):
        print("[UI] VOL_ROTARY:", direction)
        if (self.mainControlQueue != None):
            self.mainControlQueue.put(['volume_rotary', direction])

    def vol_sw_short(self):
        print("[UI] VOL_SW SHORT")
        if (self.mainControlQueue != None):
            self.mainControlQueue.put(['volume_switch', 'short'])

    def vol_sw_long(self):
        print("[UI] VOL_SW LONG")
        if (self.mainControlQueue != None):
            self.mainControlQueue.put(['volume_switch', 'long'])

    def ctrl_rotary_callback(self, direction):
        print("[UI] CTRL_ROTARY:", direction)
        if (self.mainControlQueue != None):
            self.mainControlQueue.put(['control_rotary', direction])

    def ctrl_sw_short(self):
        print("[UI] CTRL_SW SHORT")
        if (self.mainControlQueue != None):
            self.mainControlQueue.put(['control_switch', 'short'])

    def ctrl_sw_long(self):
        print("[UI] CTRL_SW LONG")
        if (self.mainControlQueue != None):
            self.mainControlQueue.put(['control_switch', 'long'])
