from flask import request as flask_request

from splitFlapClockRadioBackend.appInterface import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson

def defineSpotifyRoutes(app: App):


    @app.webserverTh.flaskApp.route('/get-spotify-status', methods=['GET'])
    def getSpotifyStatus():
        return prettyJson(app.spotifyPlayer.getStatus())

    @app.webserverTh.flaskApp.route('/spotify-search', methods=['POST'])
    def spotifySearch():
        content = flask_request.get_json(silent=True)
        ans = app.spotifyPlayer.searchSpotify(content['type'], content['terms'])
        return prettyJson(ans)

    @app.webserverTh.flaskApp.route('/spotify-play', methods=['GET'])
    def spotifyPlay():
        uri = flask_request.args.get('uri')
        app.radioTunerTh.pause()
        ans = app.spotifyPlayer.play(uri)
        return prettyJson(ans)

    @app.webserverTh.flaskApp.route('/get-spotify-auth', methods=['GET'])
    def getSpotifyAuth():
        return prettyJson(app.spotifyPlayer.getAuth())

    @app.webserverTh.flaskApp.route('/spotify-check-device', methods=['GET'])
    def spotifyCheckDevice():
        return prettyJson({'Visible': app.spotifyPlayer.check_local_device()})

    @app.webserverTh.flaskApp.route('/spotify-auth-start', methods=['GET'])
    def spotifyAuthStart():
        return prettyJson({'url': app.spotifyPlayer.startAuthProcess()})

    @app.webserverTh.flaskApp.route('/spotify-auth-end', methods=['GET'])
    def spotifyAuthEnd():
        code = flask_request.args.get('code')
        return prettyJson({'status': app.spotifyPlayer.endAuthProcess(code)})

    @app.webserverTh.flaskApp.route('/spotify-update-raspotify', methods=['POST'])
    def spotifyUpdateRaspotify():
        content = flask_request.get_json(silent=True)
        username = content['username']
        password = content['password']
        return prettyJson({'status': app.spotifyPlayer.updateRaspotifyCredentials(username, password)})

    @app.webserverTh.sio.on('spotify')
    def spotify_event(data):
        print('Spotify event!')
        print(data)
        cmd = data[0]
        arg = data[1]
        app.radioTunerTh.pause()
        if (cmd == 'next'):
            app.spotifyPlayer.next()
        if (cmd == 'previous'):
            app.spotifyPlayer.previous()
        if (cmd == 'play'):
            app.spotifyPlayer.play()
        if (cmd == 'pause'):
            app.spotifyPlayer.pause()


