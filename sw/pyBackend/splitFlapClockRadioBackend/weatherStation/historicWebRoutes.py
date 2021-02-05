from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from flask import request as flask_request

def defineHistoricWebRoutes(app: App):

    @app.webserver.flaskApp.route('/rest/historic/get-measurements', methods=['POST'])
    def getMeasurements():
        content = flask_request.get_json(silent=True)
        measurements = app.dbCtl.loadMeasurements(content['startDate'], content['stopDate']).all()
        return prettyJson(measurements)
