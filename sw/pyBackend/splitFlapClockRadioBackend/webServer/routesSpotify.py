from flask import Flask
from flask import request as flask_request
from flask_socketio import SocketIO

from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.radioTuner.radioTunerThread import RadioTunerThread
from splitFlapClockRadioBackend.spotifyPlayer.spotifyPlayer import SpotifyPlayer
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getDateTime



def defineSpotifyRoutes(app : Flask, sio : SocketIO, config : Config, spotifyPlayer: SpotifyPlayer, radioTunerTh: RadioTunerThread):


    @app.route('/get-spotify-status', methods=['GET'])
    def getSpotifyStatus():
        return prettyJson(spotifyPlayer.getStatus())

    @app.route('/spotify-search', methods=['POST'])
    def spotifySearch():
        content = flask_request.get_json(silent=True)
        ans = spotifyPlayer.searchSpotify(content['type'], content['terms'])
        return prettyJson(ans)

    @app.route('/spotify-play', methods=['GET'])
    def spotifyPlay():
        uri = flask_request.args.get('uri')
        radioTunerTh.pause()
        ans = spotifyPlayer.play(uri)
        return prettyJson(ans)

    @app.route('/get-spotify-auth', methods=['GET'])
    def getSpotifyAuth():
        return prettyJson(spotifyPlayer.getAuth())

    @app.route('/spotify-check-device', methods=['GET'])
    def spotifyCheckDevice():
        return prettyJson({'Visible': spotifyPlayer.check_local_device()})

    @app.route('/spotify-auth-start', methods=['GET'])
    def spotifyAuthStart():
        return prettyJson({'url': spotifyPlayer.startAuthProcess()})

    @app.route('/spotify-auth-end', methods=['GET'])
    def spotifyAuthEnd():
        code = flask_request.args.get('code')
        return prettyJson({'status': spotifyPlayer.endAuthProcess(code)})

    @app.route('/spotify-update-raspotify', methods=['POST'])
    def spotifyUpdateRaspotify():
        content = flask_request.get_json(silent=True)
        username = content['username']
        password = content['password']
        return prettyJson({'status': spotifyPlayer.updateRaspotifyCredentials(username, password)})

    @sio.on('spotify')
    def spotify_event(data):
        print('Spotify event!')
        print(data)
        cmd = data[0]
        arg = data[1]
        radioTunerTh.pause()
        if (cmd == 'next'):
            spotifyPlayer.next()
        if (cmd == 'previous'):
            spotifyPlayer.previous()
        if (cmd == 'play'):
            spotifyPlayer.play()
        if (cmd == 'pause'):
            spotifyPlayer.pause()


