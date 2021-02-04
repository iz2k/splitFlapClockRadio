from flask import request as flask_request

from splitFlapClockRadioBackend.__main__ import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson

def defineRadioTunerWebRoutes(app: App):

    @app.webserver.flaskApp.route('/get-radio-status', methods=['GET'])
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


    @app.webserver.flaskApp.route('/set-radio-tune', methods=['GET'])
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




