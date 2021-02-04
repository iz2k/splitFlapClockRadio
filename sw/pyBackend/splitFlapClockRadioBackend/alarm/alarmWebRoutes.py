from flask import request as flask_request

from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.timeTools import getDateTime



def defineAlarmWebRoutes(app: App):

    @app.webserver.flaskApp.route('/get-alarm-list', methods=['GET'])
    def getAlarms():
        return prettyJson(app.config.params['clock']['alarms'])


    @app.webserver.flaskApp.route('/set-alarm', methods=['POST'])
    def setAlarm():
        content = flask_request.get_json(silent=True)
        if (content != None):
            if (len(content)==2):
                app.config.updateClockAlarm(content[0], content[1])
                app.alarm.loadAlarms()
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
