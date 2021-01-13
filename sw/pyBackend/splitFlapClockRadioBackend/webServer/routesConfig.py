from flask import Flask
from flask import request as flask_request

from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


def defineConfigRoutes(app : Flask, config : Config):

    @app.route('/get-location-config', methods=['GET'])
    def getLocationConfig():
        return prettyJson(config.params['location'])

    @app.route('/get-api-config', methods=['GET'])
    def getApis():
        return prettyJson(config.params['api'])

    @app.route('/get-sensors-config', methods=['GET'])
    def getSensors():
        return prettyJson(config.params['sensors'])

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/set-api', methods=['GET'])
    def setApi():
        try:
            # Get arguments
            for parameter in flask_request.args:
                value = flask_request.args.get(parameter)
                # Update parameter
                config.updateApiParam(parameter,value)
            return prettyJson(config.params['api'])
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/set-location', methods=['GET'])
    def setLocation():
        try:
            # Get arguments
            for parameter in flask_request.args:
                value = flask_request.args.get(parameter)
                # Update parameter
                config.updateLocationParam(parameter, value)
            return prettyJson(config.params['location'])
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/set-sensors', methods=['GET'])
    def setSensors():
        try:
            # Get arguments
            for parameter in flask_request.args:
                value = flask_request.args.get(parameter)
                # Update parameter
                config.updateSensorParam(parameter, value)
            return prettyJson(config.params['sensors'])
        except Exception as e:
            print(e)
            return 'Invalid parameters'
