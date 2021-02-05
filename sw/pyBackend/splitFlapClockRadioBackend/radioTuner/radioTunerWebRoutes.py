from flask import request as flask_request

from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson

def defineRadioTunerWebRoutes(app: App):

    @app.webserver.flaskApp.route('/rest/radio/get-status', methods=['GET'])
    def getRadioStatus():
        return prettyJson(app.radioTuner.lastReport)

    @app.webserver.sio.on('fmRadio')
    def fmRadio_event(data):
        cmd = data[0]
        arg = data[1]
        app.spotifyPlayer.pause()
        if (cmd == 'seek_up'):
            app.radioTuner.next()
        if (cmd == 'seek_down'):
            app.radioTuner.previous()
        if (cmd == 'turn_on'):
            if app.radioTuner.radioTuner.on == False:
                app.radioTuner.tune(97.2)
            app.radioTuner.play()
        if (cmd == 'turn_off'):
            app.radioTuner.pause()


    @app.webserver.flaskApp.route('/rest/radio/tune', methods=['GET'])
    def setRadioTune():
        try:
            # Get arguments
            freq = float(flask_request.args.get('freq'))
            app.spotifyPlayer.pause()
            app.radioTuner.tune(freq)
            app.radioTuner.play()
            return prettyJson({'status' : 'Tuning ' + str(freq) + '!'})
        except Exception as e:
            print(e)
            return 'Invalid freq to tune'


    @app.webserver.flaskApp.route('/rest/radio/get-items', methods=['GET'])
    def getRadioItems():
        return prettyJson(app.config.params['radioItems'])

    @app.webserver.flaskApp.route('/rest/radio/add-item', methods=['POST'])
    def addRadioItem():
        content = flask_request.get_json(silent=True)
        if (content != None):
            if (len(content)==2):
                app.config.addRadioItem(content[0], content[1])
        return prettyJson({'status' : 'Adding Radio Item!'})

    # /url?arg1=xxxx&arg2=yyy
    @app.webserver.flaskApp.route('/rest/radio/delete-item', methods=['GET'])
    def deleteRadioItem():
        try:
            # Get arguments
            idx = flask_request.args.get('idx')
            app.config.deleteRadioItem(int(idx))
            return prettyJson({'status' : 'RadioItem Deleted!'})
        except Exception as e:
            print(e)
            return 'Invalid idx to delete alarm'
