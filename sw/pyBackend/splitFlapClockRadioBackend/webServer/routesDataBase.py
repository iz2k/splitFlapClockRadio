from flask import Flask
from flask import request as flask_request

from splitFlapClockRadioBackend.dbManager.dbController import dbController
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


def defineDataBaseRoutes(app : Flask, dbCtl : dbController):

    @app.route('/get-measurements', methods=['POST'])
    def getMeasurements():
        content = flask_request.get_json(silent=True)
        print(content)
        measurements = dbCtl.loadMeasurements(content['startDate'], content['stopDate']).all()
        return prettyJson(measurements)
