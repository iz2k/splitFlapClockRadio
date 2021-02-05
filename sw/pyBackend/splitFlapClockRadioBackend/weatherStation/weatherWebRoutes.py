from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from flask import request as flask_request

def defineWeatherWebRoutes(app: App):

    @app.webserver.flaskApp.route('/rest/weather/get-current', methods=['GET'])
    def getWeather():
        return prettyJson(app.weatherStation.weatherReport)

    @app.webserver.flaskApp.route('/rest/weather/reload', methods=['GET'])
    def reloadWeather():
        app.weatherStation.reloadWeather()
        app.webserver.sio.emit('weatherReport', app.weatherStation.weatherReport)
        return prettyJson({'status':'Success'})

    @app.webserver.flaskApp.route('/rest/weather/get-apis', methods=['GET'])
    def getApis():
        return prettyJson(app.config.params['api'])

    # /url?arg1=xxxx&arg2=yyy
    @app.webserver.flaskApp.route('/rest/weather/set-apis', methods=['GET'])
    def setApis():
        try:
            # Get arguments
            for parameter in flask_request.args:
                value = flask_request.args.get(parameter)
                # Update parameter
                app.config.updateApiParam(parameter,value)
            return prettyJson(app.config.params['api'])
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    @app.webserver.flaskApp.route('/rest/weather/get-location', methods=['GET'])
    def getLocation():
        return prettyJson(app.config.params['location'])

    # /url?arg1=xxxx&arg2=yyy
    @app.webserver.flaskApp.route('/rest/weather/set-location', methods=['GET'])
    def setLocation():
        try:
            # Get arguments
            for parameter in flask_request.args:
                value = flask_request.args.get(parameter)
                # Update parameter
                app.config.updateLocationParam(parameter, value)
            return prettyJson(app.config.params['location'])
        except Exception as e:
            print(e)
            return 'Invalid parameters'


