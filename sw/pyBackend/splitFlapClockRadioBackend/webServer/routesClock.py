from flask import Flask

from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getDateTime



def defineClockRoutes(app : Flask, config : Config):

    @app.route('/get-time', methods=['GET'])
    def getTime():
        print(config.params['clock']['timeZone'])
        return prettyJson(getDateTime(config.params['clock']['timeZone']))







