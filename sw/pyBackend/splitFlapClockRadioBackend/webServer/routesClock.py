from flask import Flask

from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getDateTime


def defineClockRoutes(app : Flask):

    @app.route('/get-time', methods=['GET'])
    def getTime():
        return prettyJson(getDateTime())








