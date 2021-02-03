from splitFlapClockRadioBackend.appInterface import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


def defineWeatherStationRoutes(app: App):

    @app.webserverTh.flaskApp.route('/get-weather', methods=['GET'])
    def getWeather():
        return prettyJson(app.weatherStationTh.weatherStation.weatherReport)

    @app.webserverTh.flaskApp.route('/get-sensors', methods=['GET'])
    def getHome():
        return prettyJson(app.weatherStationTh.weatherStation.sensorReport)

    @app.webserverTh.flaskApp.route('/reset-sensors-baseline', methods=['GET'])
    def resetBaseline():
        return prettyJson(app.weatherStationTh.weatherStation.sgp.resetBaseline())

    @app.webserverTh.flaskApp.route('/reload-sensors', methods=['GET'])
    def reloadSensors():
        app.weatherStationTh.weatherStation.reloadSensors()
        return prettyJson({'status':'Success'})

    @app.webserverTh.flaskApp.route('/reload-weather', methods=['GET'])
    def reloadWeather():
        app.weatherStationTh.weatherStation.reloadWeather()
        app.webserverTh.sio.emit('weatherReport', app.weatherStationTh.weatherStation.weatherReport)
        return prettyJson({'status':'Success'})
