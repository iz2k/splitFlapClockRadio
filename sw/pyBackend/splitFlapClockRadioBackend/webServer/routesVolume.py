from flask import request as flask_request

from splitFlapClockRadioBackend.appInterface import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson



def defineVolumeRoutes(app: App):

    @app.webserverTh.flaskApp.route('/get-volume', methods=['GET'])
    def getVolume():
        return prettyJson({'mute': app.audio.mute, 'volume': app.audio.volume})

    @app.webserverTh.flaskApp.route('/set-volume', methods=['GET'])
    def setVolume():
        value = flask_request.args.get('vol')
        app.audio.set_volume(int(value))
        return prettyJson({'mute': app.audio.mute, 'volume': app.audio.volume})

    @app.webserverTh.flaskApp.route('/toggle-mute', methods=['GET'])
    def toggleMute():
        app.audio.toggle_mute()
        return prettyJson({'mute': app.audio.mute, 'volume': app.audio.volume})
