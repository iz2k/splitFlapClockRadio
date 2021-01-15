from flask import Flask
from flask import request as flask_request

from splitFlapClockRadioBackend.clock.clockThread import ClockThread
from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getDateTime



def defineClockRoutes(app : Flask, config : Config, clockTh : ClockThread):

    @app.route('/get-time', methods=['GET'])
    def getTime():
        print(config.params['clock']['timeZone'])
        return prettyJson(getDateTime(config.params['clock']['timeZone']))

    @app.route('/get-clock-mode', methods=['GET'])
    def getClockMode():
        return prettyJson(clockTh.mode)

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/set-clock-mode', methods=['GET'])
    def setClockMode():
        try:
            # Get arguments
            for parameter in flask_request.args:
                value = flask_request.args.get(parameter)
                # Update mode parameter
                if(parameter == 'mode'):
                    clockTh.mode = value
            return prettyJson(clockTh.mode)
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/get-clock-status', methods=['GET'])
    def getClockStatus():
        try:
            return prettyJson(clockTh.smbus430.getFlapStatus(flask_request.args['type']))
        except Exception as e:
            print(e)
            return 'Invalid parameters. Please specify type=hh, mm or ww'

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/set-clock-parameter', methods=['GET'])
    def setClockParameter():
        try:
            return prettyJson(clockTh.smbus430.setFlapParameter(flask_request.args['type'], flask_request.args['parameter'], int(flask_request.args['value'])))
        except Exception as e:
            print(e)
            return 'Invalid parameters. Please specify type=hh, mm or ww'






