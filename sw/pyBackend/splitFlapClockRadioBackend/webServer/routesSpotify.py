from flask import Flask
from flask_socketio import SocketIO

from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.spotifyPlayer.spotifyPlayer import SpotifyPlayer
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getDateTime



def defineSpotifyRoutes(app : Flask, sio : SocketIO, config : Config, spotifyPlayer: SpotifyPlayer):


    @app.route('/get-spotify-status', methods=['GET'])
    def getSpotifyStatus():
        return prettyJson(spotifyPlayer.getStatus())

    @sio.on('spotify')
    def fmRadio_event(data):
        print('Spotify event!')
        print(data)
        cmd = data[0]
        arg = data[1]
        if (cmd == 'next'):
            spotifyPlayer.next()
        if (cmd == 'previous'):
            spotifyPlayer.previous()
        if (cmd == 'play'):
            spotifyPlayer.play()
        if (cmd == 'pause'):
            spotifyPlayer.pause()


