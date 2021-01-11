from flask import Flask
from flask import request as flask_request
from flask_socketio import SocketIO

from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.weatherStation.weatherStation import WeatherStation


def defineWeatherStationRoutes(app : Flask, sio : SocketIO, weather : WeatherStation, config : Config):

    @app.route('/get-location-config', methods=['GET'])
    def getWeatherConfig():
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
            weather.reloadConfig()
            return prettyJson(config.params['location'])
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    @app.route('/get-weather', methods=['GET'])
    def getWeather():
        return prettyJson(weather.weatherReport)

    @app.route('/get-home', methods=['GET'])
    def getHome():
        return prettyJson(weather.sensorReport)

    @app.route('/reset-baseline', methods=['GET'])
    def resetBaseline():
        return prettyJson(weather.sgp.resetBaseline())

    @app.route('/reload-sensors', methods=['GET'])
    def reloadSensors():
        weather.reloadConfig()
        return prettyJson({'status':'Success'})
