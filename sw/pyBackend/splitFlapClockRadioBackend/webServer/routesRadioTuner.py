from flask import Flask
from flask_socketio import SocketIO
from flask import request as flask_request

from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.radioTuner.radioTunerThread import RadioTunerThread
from splitFlapClockRadioBackend.spotifyPlayer.spotifyPlayer import SpotifyPlayer
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getDateTime



def defineRadioTunerRoutes(app : Flask, sio : SocketIO, config : Config, radioTunerTh: RadioTunerThread, spotifyPlayer: SpotifyPlayer):

    @app.route('/get-radio-status', methods=['GET'])
    def getRadioStatus():
        return prettyJson(radioTunerTh.lastReport)

    @sio.on('fmRadio')
    def fmRadio_event(data):
        cmd = data[0]
        arg = data[1]
        spotifyPlayer.pause()
        if (cmd == 'seek_up'):
            radioTunerTh.next()
        if (cmd == 'seek_down'):
            radioTunerTh.previous()
        if (cmd == 'turn_on'):
            radioTunerTh.play()
        if (cmd == 'turn_off'):
            radioTunerTh.pause()


    @app.route('/set-radio-tune', methods=['GET'])
    def setRadioTune():
        try:
            # Get arguments
            freq = float(flask_request.args.get('freq'))
            spotifyPlayer.pause()
            radioTunerTh.tune(freq)
            radioTunerTh.play()
            return prettyJson({'status' : 'Tuning ' + str(freq) + '!'})
        except Exception as e:
            print(e)
            return 'Invalid freq to tune'




