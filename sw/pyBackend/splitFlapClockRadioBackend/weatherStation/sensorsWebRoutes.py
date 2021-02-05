from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from flask import request as flask_request

def defineSensorsWebRoutes(app: App):


    @app.webserver.flaskApp.route('/rest/sensors/get-current', methods=['GET'])
    def getSensors():
        return prettyJson(app.weatherStation.sensorReport)

    @app.webserver.flaskApp.route('/rest/sensors/get-config', methods=['GET'])
    def getSensorsConfig():
        return prettyJson(app.config.params['sensors'])

    @app.webserver.flaskApp.route('/rest/sensors/reset-baseline', methods=['GET'])
    def resetBaseline():
        return prettyJson(app.weatherStation.sgp.resetBaseline())

    @app.webserver.flaskApp.route('/rest/sensors/reload', methods=['GET'])
    def reloadSensors():
        app.weatherStation.reloadSensors()
        return prettyJson({'status':'Success'})

    # /url?arg1=xxxx&arg2=yyy
    @app.webserver.flaskApp.route('/rest/sensors/set-params', methods=['GET'])
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
