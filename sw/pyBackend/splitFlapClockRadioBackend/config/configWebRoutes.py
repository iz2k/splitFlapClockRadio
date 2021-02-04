from flask import request as flask_request

from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson


def defineConfigWebRoutes(app: App):

    @app.webserver.flaskApp.route('/get-location-config', methods=['GET'])
    def getLocationConfig():
        return prettyJson(app.config.params['location'])

    @app.webserver.flaskApp.route('/get-api-config', methods=['GET'])
    def getApis():
        return prettyJson(app.config.params['api'])

    @app.webserver.flaskApp.route('/get-sensors-config', methods=['GET'])
    def getSensors():
        return prettyJson(app.config.params['sensors'])

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

    @app.webserver.flaskApp.route('/set-timezone', methods=['POST'])
    def setTimezone():
        content = flask_request.get_json(silent=True)
        if (content != None):
            app.config.updateClockParam('timeZone', content['nameValue'])
        return prettyJson({'status' : 'Timezone modified!'})

    @app.webserver.flaskApp.route('/get-alarm-list', methods=['GET'])
    def getAlarms():
        return prettyJson(app.config.params['clock']['alarms'])


    @app.webserver.flaskApp.route('/set-alarm', methods=['POST'])
    def setAlarm():
        content = flask_request.get_json(silent=True)
        if (content != None):
            if (len(content)==2):
                app.config.updateClockAlarm(content[0], content[1])
        print('[alarm] Updating alarm >> ' + content[1]['Name'] + ' <<')
        return prettyJson({'status' : 'Updating alarm!'})

    # /url?arg1=xxxx&arg2=yyy
    @app.webserver.flaskApp.route('/delete-alarm', methods=['GET'])
    def deleteAlarm():
        try:
            # Get arguments
            idx = flask_request.args.get('idx')
            app.config.deleteClockAlarm(int(idx))
            return prettyJson({'status' : 'Alarm Deleted!'})
        except Exception as e:
            print(e)
            return 'Invalid idx to delete alarm'

    @app.webserver.flaskApp.route('/get-radio-items', methods=['GET'])
    def getRadioItems():
        return prettyJson(app.config.params['radioItems'])

    @app.webserver.flaskApp.route('/add-radio-item', methods=['POST'])
    def addRadioItem():
        content = flask_request.get_json(silent=True)
        if (content != None):
            if (len(content)==2):
                app.config.addRadioItem(content[0], content[1])
        return prettyJson({'status' : 'Adding Radio Item!'})

    # /url?arg1=xxxx&arg2=yyy
    @app.webserver.flaskApp.route('/delete-radio-item', methods=['GET'])
    def deleteRadioItem():
        try:
            # Get arguments
            idx = flask_request.args.get('idx')
            app.config.deleteRadioItem(int(idx))
            return prettyJson({'status' : 'RadioItem Deleted!'})
        except Exception as e:
            print(e)
            return 'Invalid idx to delete alarm'

    @app.webserver.flaskApp.route('/get-spotify-items', methods=['GET'])
    def getSpotifyItems():
        return prettyJson(app.config.params['spotifyItems'])

    @app.webserver.flaskApp.route('/add-spotify-item', methods=['POST'])
    def addSpotifyItem():
        try:
            # Get arguments
            content = flask_request.get_json(silent=True)
            app.config.addSpotifyItem(content['Type'], content['Name'], content['URI'], content['Image'])
            app.webserver.sio.emit('spotifyItems', prettyJson(app.config.params['spotifyItems']))
            return prettyJson({'status': 'Adding Spotify Item!'})
        except Exception as e:
            print(e)
            return 'Invalid args to add spotify item'

    # /url?arg1=xxxx&arg2=yyy
    @app.webserver.flaskApp.route('/delete-spotify-item', methods=['GET'])
    def deleteSpotifyItem():
        try:
            # Get arguments
            idx = flask_request.args.get('idx')
            app.config.deletepotifyItem(int(idx))
            return prettyJson({'status': 'Spotify Item Deleted!'})
        except Exception as e:
            print(e)
            return 'Invalid idx to delete spotify item'
