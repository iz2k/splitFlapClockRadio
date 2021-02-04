from flask import request as flask_request

from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson

def defineSpotifyPlayerWebRoutes(app: App):


    @app.webserver.flaskApp.route('/get-spotify-status', methods=['GET'])
    def getSpotifyStatus():
        return prettyJson(app.spotifyPlayer.getStatus())

    @app.webserver.flaskApp.route('/spotify-search', methods=['POST'])
    def spotifySearch():
        content = flask_request.get_json(silent=True)
        ans = app.spotifyPlayer.searchSpotify(content['type'], content['terms'])
        return prettyJson(ans)

    @app.webserver.flaskApp.route('/spotify-play', methods=['GET'])
    def spotifyPlay():
        uri = flask_request.args.get('uri')
        app.radioTuner.pause()
        ans = app.spotifyPlayer.play(uri)
        return prettyJson(ans)

    @app.webserver.flaskApp.route('/get-spotify-auth', methods=['GET'])
    def getSpotifyAuth():
        return prettyJson(app.spotifyPlayer.getAuth())

    @app.webserver.flaskApp.route('/spotify-check-device', methods=['GET'])
    def spotifyCheckDevice():
        return prettyJson({'Visible': app.spotifyPlayer.check_local_device()})

    @app.webserver.flaskApp.route('/spotify-auth-start', methods=['GET'])
    def spotifyAuthStart():
        return prettyJson({'url': app.spotifyPlayer.startAuthProcess()})

    @app.webserver.flaskApp.route('/spotify-auth-end', methods=['GET'])
    def spotifyAuthEnd():
        code = flask_request.args.get('code')
        return prettyJson({'status': app.spotifyPlayer.endAuthProcess(code)})

    @app.webserver.flaskApp.route('/spotify-update-raspotify', methods=['POST'])
    def spotifyUpdateRaspotify():
        content = flask_request.get_json(silent=True)
        username = content['username']
        password = content['password']
        return prettyJson({'status': app.spotifyPlayer.updateRaspotifyCredentials(username, password)})

    @app.webserver.sio.on('spotify')
    def spotify_event(data):
        cmd = data[0]
        arg = data[1]
        app.radioTuner.pause()
        if (cmd == 'next'):
            app.spotifyPlayer.next()
        if (cmd == 'previous'):
            app.spotifyPlayer.previous()
        if (cmd == 'play'):
            app.spotifyPlayer.play()
        if (cmd == 'pause'):
            app.spotifyPlayer.pause()


