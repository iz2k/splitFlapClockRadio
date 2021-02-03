from flask import Flask
from flask import request as flask_request

from splitFlapClockRadioBackend.audio.audio import Audio
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getDateTime



def defineVolumeRoutes(app : Flask, audio : Audio):

    @app.route('/get-volume', methods=['GET'])
    def getVolume():
        return prettyJson({'mute': audio.mute, 'volume': audio.volume})

    @app.route('/set-volume', methods=['GET'])
    def setVolume():
        value = flask_request.args.get('vol')
        audio.set_volume(int(value))
        return prettyJson({'mute': audio.mute, 'volume': audio.volume})

    @app.route('/toggle-mute', methods=['GET'])
    def toggleMute():
        audio.toggle_mute()
        return prettyJson({'mute': audio.mute, 'volume': audio.volume})
