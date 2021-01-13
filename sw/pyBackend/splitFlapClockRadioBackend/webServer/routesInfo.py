from flask_socketio import SocketIO

from splitFlapClockRadioBackend.osInfo.osInfoThread import getReport
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


def defineInfoRoutes(sio : SocketIO):

    @sio.on('connect')
    def onconnect_event():
        print('Client connected!')
        sio.emit('osInfo', prettyJson(getReport()))

    @sio.on('disconnect')
    def ondisconnect_event():
        print('Client disconnected!')

