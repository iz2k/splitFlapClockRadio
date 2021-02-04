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
        app.spotifyPlayer.check_local_device()
        return prettyJson({'Visible': app.spotifyPlayer.check_local_device()})

    @app.webserver.flaskApp.route('/spotify-auth-start', methods=['GET'])
    def spotifyAuthStart():
        app.spotifyPlayer.spotipyAuth.startAuthProcess()
        return prettyJson({'status': 'Spotipy authentication process started'})

    @app.webserver.flaskApp.route('/spotify-auth-url', methods=['GET'])
    def spotifyAuthUrl():
        return prettyJson({'url': app.spotifyPlayer.spotipyAuth.url})

    @app.webserver.flaskApp.route('/spotify-auth-end', methods=['GET'])
    def spotifyAuthEnd():
        code = flask_request.args.get('code')
        app.spotifyPlayer.spotipyAuth.endAuthProcess(code)
        return prettyJson({'status': 'Spotipy authentication process ended'})

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

    @app.webserver.flaskApp.route('/get-spotify-items', methods=['GET'])
    def getSpotifyItems():
        return prettyJson(app.config.params['spotifyItems'])

    @app.webserver.flaskApp.route('/add-spotify-item', methods=['POST'])
    def addSpotifyItem():
        try:
            # Get arguments
            content = flask_request.get_json(silent=True)
            app.config.addSpotifyItem(content['Type'], content['Name'], content['URI'], content['Image'])
            app.webserver.sio.emit('spotifyItems', prettyJson(app.config.params['spotifyItems']))
            return prettyJson({'status': 'Adding Spotify Item!'})
        except Exception as e:
            print(e)
            return 'Invalid args to add spotify item'

    # /url?arg1=xxxx&arg2=yyy
    @app.webserver.flaskApp.route('/delete-spotify-item', methods=['GET'])
    def deleteSpotifyItem():
        try:
            # Get arguments
            idx = flask_request.args.get('idx')
            app.config.deletepotifyItem(int(idx))
            return prettyJson({'status': 'Spotify Item Deleted!'})
        except Exception as e:
            print(e)
            return 'Invalid idx to delete spotify item'
