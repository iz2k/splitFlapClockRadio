from splitFlapClockRadioBackend.appInterface import App
from splitFlapClockRadioBackend.osInfo.osInfoThread import getReport
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


def defineInfoRoutes(app: App):

    @app.webserverTh.sio.on('connect')
    def onconnect_event():
        app.webserverTh.sio.emit('osInfo', prettyJson(getReport()))


