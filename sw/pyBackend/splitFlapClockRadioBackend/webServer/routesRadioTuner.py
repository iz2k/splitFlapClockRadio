from flask import Flask
from flask_socketio import SocketIO

from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.radioTuner.radioTunerThread import RadioTunerThread
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getDateTime



def defineRadioTunerRoutes(app : Flask, sio : SocketIO, config : Config, radioTunerTh: RadioTunerThread):

    @app.route('/get-radio-status', methods=['GET'])
    def getRadioStatus():
        return prettyJson(radioTunerTh.lastReport)

    @sio.on('fmRadio')
    def fmRadio_event(data):
        cmd = data[0]
        arg = data[1]
        if (cmd == 'seek_up'):
            radioTunerTh.next()
        if (cmd == 'seek_down'):
            radioTunerTh.previous()
        if (cmd == 'turn_on'):
            radioTunerTh.play()
        if (cmd == 'turn_off'):
            radioTunerTh.pause()
        print('Radio event!')
        print(data)






