from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from flask import request as flask_request

def defineWeatherStationWebRoutes(app: App):

    @app.webserver.flaskApp.route('/get-weather', methods=['GET'])
    def getWeather():
        return prettyJson(app.weatherStation.weatherReport)

    @app.webserver.flaskApp.route('/reload-weather', methods=['GET'])
    def reloadWeather():
        app.weatherStation.reloadWeather()
        app.webserver.sio.emit('weatherReport', app.weatherStation.weatherReport)
        return prettyJson({'status':'Success'})

    @app.webserver.flaskApp.route('/get-sensors', methods=['GET'])
    def getSensors():
        return prettyJson(app.weatherStation.sensorReport)

    @app.webserver.flaskApp.route('/get-sensors-config', methods=['GET'])
    def getSensorsConfig():
        return prettyJson(app.config.params['sensors'])

    @app.webserver.flaskApp.route('/reset-sensors-baseline', methods=['GET'])
    def resetBaseline():
        return prettyJson(app.weatherStation.sgp.resetBaseline())

    @app.webserver.flaskApp.route('/reload-sensors', methods=['GET'])
    def reloadSensors():
        app.weatherStation.reloadSensors()
        return prettyJson({'status':'Success'})

    @app.webserver.flaskApp.route('/get-measurements', methods=['POST'])
    def getMeasurements():
        content = flask_request.get_json(silent=True)
        measurements = app.dbCtl.loadMeasurements(content['startDate'], content['stopDate']).all()
        return prettyJson(measurements)

    @app.webserver.flaskApp.route('/get-location-config', methods=['GET'])
    def getLocationConfig():
        return prettyJson(app.config.params['location'])

    @app.webserver.flaskApp.route('/get-api-config', methods=['GET'])
    def getApis():
        return prettyJson(app.config.params['api'])

    # /url?arg1=xxxx&arg2=yyy
    @app.webserver.flaskApp.route('/set-api', methods=['GET'])
    def setApi():
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

    # /url?arg1=xxxx&arg2=yyy
    @app.webserver.flaskApp.route('/set-location', methods=['GET'])
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

    # /url?arg1=xxxx&arg2=yyy
    @app.webserver.flaskApp.route('/set-sensors', methods=['GET'])
    def setSensors():
        try:
            # Get arguments
            for parameter in flask_request.args:
                value = flask_request.args.get(parameter)
                # Update parameter
                app.config.updateSensorParam(parameter, value)
            return prettyJson(app.config.params['sensors'])
        except Exception as e:
            print(e)
            return 'Invalid parameters'
