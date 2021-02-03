from flask import request as flask_request

from splitFlapClockRadioBackend.appInterface import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


def defineDataBaseRoutes(app: App):

    @app.webserverTh.flaskApp.route('/get-measurements', methods=['POST'])
    def getMeasurements():
        content = flask_request.get_json(silent=True)
        print(content)
        measurements = app.dbCtl.loadMeasurements(content['startDate'], content['stopDate']).all()
        return prettyJson(measurements)
