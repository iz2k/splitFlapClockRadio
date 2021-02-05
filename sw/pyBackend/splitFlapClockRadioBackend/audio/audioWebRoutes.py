from flask import request as flask_request

from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson



def defineAudioWebRoutes(app: App):

    @app.webserver.flaskApp.route('/rest/audio/get-volume', methods=['GET'])
    def getVolume():
        return prettyJson({'mute': app.audio.mute, 'volume': app.audio.volume})

    @app.webserver.flaskApp.route('/rest/audio/set-volume', methods=['GET'])
    def setVolume():
        value = flask_request.args.get('vol')
        app.audio.set_volume(int(value))
        return prettyJson({'mute': app.audio.mute, 'volume': app.audio.volume})

    @app.webserver.flaskApp.route('/rest/audio/toggle-mute', methods=['GET'])
    def toggleMute():
        app.audio.toggle_mute()
        return prettyJson({'mute': app.audio.mute, 'volume': app.audio.volume})
