from flask import Flask
from flask_socketio import SocketIO

from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.weatherStation.weatherStation import WeatherStation


def defineWeatherStationRoutes(app : Flask, sio :  SocketIO, weather : WeatherStation):

    @app.route('/get-weather', methods=['GET'])
    def getWeather():
        return prettyJson(weather.weatherReport)

    @app.route('/get-sensors', methods=['GET'])
    def getHome():
        return prettyJson(weather.sensorReport)

    @app.route('/reset-sensors-baseline', methods=['GET'])
    def resetBaseline():
        return prettyJson(weather.sgp.resetBaseline())

    @app.route('/reload-sensors', methods=['GET'])
    def reloadSensors():
        weather.reloadSensors()
        return prettyJson({'status':'Success'})

    @app.route('/reload-weather', methods=['GET'])
    def reloadWeather():
        weather.reloadWeather()
        sio.emit('weatherReport', weather.weatherReport)
        return prettyJson({'status':'Success'})
