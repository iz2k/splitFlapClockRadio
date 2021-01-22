from flask import Flask
from flask import request as flask_request

from splitFlapClockRadioBackend.config.config import Config
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


def defineConfigRoutes(app : Flask, config : Config):

    @app.route('/get-location-config', methods=['GET'])
    def getLocationConfig():
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
            return prettyJson(config.params['location'])
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/set-sensors', methods=['GET'])
    def setSensors():
        try:
            # Get arguments
            for parameter in flask_request.args:
                value = flask_request.args.get(parameter)
                # Update parameter
                config.updateSensorParam(parameter, value)
            return prettyJson(config.params['sensors'])
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    @app.route('/set-timezone', methods=['POST'])
    def setTimezone():
        content = flask_request.get_json(silent=True)
        if (content != None):
            config.updateClockParam('timeZone', content['nameValue'])
        return prettyJson({'status' : 'Timezone modified!'})

    @app.route('/get-alarm-list', methods=['GET'])
    def getAlarms():
        return prettyJson(config.params['clock']['alarms'])


    @app.route('/set-alarm', methods=['POST'])
    def setAlarm():
        content = flask_request.get_json(silent=True)
        if (content != None):
            if (len(content)==2):
                config.updateClockAlarm(content[0], content[1])
        return prettyJson({'status' : 'Updating alarm!'})

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/delete-alarm', methods=['GET'])
    def deleteAlarm():
        try:
            # Get arguments
            idx = flask_request.args.get('idx')
            config.deleteClockAlarm(int(idx))
            return prettyJson({'status' : 'Alarm Deleted!'})
        except Exception as e:
            print(e)
            return 'Invalid idx to delete alarm'

    @app.route('/get-radio-items', methods=['GET'])
    def getRadioItems():
        return prettyJson(config.params['radioItems'])

    @app.route('/add-radio-item', methods=['POST'])
    def addRadioItem():
        content = flask_request.get_json(silent=True)
        if (content != None):
            if (len(content)==2):
                config.addRadioItem(content[0], content[1])
        return prettyJson({'status' : 'Adding Radio Item!'})

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/delete-radio-item', methods=['GET'])
    def deleteRadioItem():
        try:
            # Get arguments
            idx = flask_request.args.get('idx')
            config.deleteRadioItem(int(idx))
            return prettyJson({'status' : 'RadioItem Deleted!'})
        except Exception as e:
            print(e)
            return 'Invalid idx to delete alarm'
