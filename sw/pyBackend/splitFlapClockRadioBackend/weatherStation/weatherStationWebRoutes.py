from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


def defineWeatherStationWebRoutes(app: App):

    @app.webserver.flaskApp.route('/get-weather', methods=['GET'])
    def getWeather():
        return prettyJson(app.weatherStation.weatherReport)

    @app.webserver.flaskApp.route('/get-sensors', methods=['GET'])
    def getHome():
        return prettyJson(app.weatherStation.sensorReport)

    @app.webserver.flaskApp.route('/reset-sensors-baseline', methods=['GET'])
    def resetBaseline():
        return prettyJson(app.weatherStation.sgp.resetBaseline())

    @app.webserver.flaskApp.route('/reload-sensors', methods=['GET'])
    def reloadSensors():
        app.weatherStation.reloadSensors()
        return prettyJson({'status':'Success'})

    @app.webserver.flaskApp.route('/reload-weather', methods=['GET'])
    def reloadWeather():
        app.weatherStation.reloadWeather()
        app.webserver.sio.emit('weatherReport', app.weatherStation.weatherReport)
        return prettyJson({'status':'Success'})
