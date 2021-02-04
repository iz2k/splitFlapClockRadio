from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.osInfo.osInfo import getReport
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


def defineOsInfoWebRoutes(app: App):

    @app.webserver.sio.on('connect')
    def onconnect_event():
        app.webserver.sio.emit('osInfo', prettyJson(getReport()))


