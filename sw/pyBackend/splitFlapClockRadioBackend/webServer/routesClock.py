from flask import request as flask_request

from splitFlapClockRadioBackend.appInterface import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getDateTime



def defineClockRoutes(app: App):

    @app.webserverTh.flaskApp.route('/get-time', methods=['GET'])
    def getTime():
        print(app.config.params['clock']['timeZone'])
        return prettyJson(getDateTime(app.config.params['clock']['timeZone']))

    @app.webserverTh.flaskApp.route('/get-clock-mode', methods=['GET'])
    def getClockMode():
        return prettyJson(app.clockTh.mode)

    # /url?arg1=xxxx&arg2=yyy
    @app.webserverTh.flaskApp.route('/set-clock-mode', methods=['GET'])
    def setClockMode():
        try:
            # Get arguments
            for parameter in flask_request.args:
                value = flask_request.args.get(parameter)
                # Update mode parameter
                if(parameter == 'mode'):
                    app.clockTh.mode = value
            return prettyJson(app.clockTh.mode)
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    # /url?arg1=xxxx&arg2=yyy
    @app.webserverTh.flaskApp.route('/get-clock-status', methods=['GET'])
    def getClockStatus():
        try:
            return prettyJson(app.clockTh.smbus430.getFlapStatus(flask_request.args['type']))
        except Exception as e:
            print(e)
            return 'Invalid parameters. Please specify type=hh, mm or ww'

    # /url?arg1=xxxx&arg2=yyy
    @app.webserverTh.flaskApp.route('/set-clock-parameter', methods=['GET'])
    def setClockParameter():
        try:
            return prettyJson(app.clockTh.smbus430.setFlapParameter(flask_request.args['type'], flask_request.args['parameter'], int(flask_request.args['value'])))
        except Exception as e:
            print(e)
            return 'Invalid parameters. Please specify type=hh, mm or ww'






