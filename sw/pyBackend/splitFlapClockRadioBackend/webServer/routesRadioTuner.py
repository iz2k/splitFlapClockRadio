from flask import request as flask_request

from splitFlapClockRadioBackend.appInterface import App
from splitFlapClockRadioBackend.tools.jsonTools import prettyJson

def defineRadioTunerRoutes(app: App):

    @app.webserverTh.flaskApp.route('/get-radio-status', methods=['GET'])
    def getRadioStatus():
        return prettyJson(app.radioTunerTh.lastReport)

    @app.webserverTh.sio.on('fmRadio')
    def fmRadio_event(data):
        cmd = data[0]
        arg = data[1]
        app.spotifyPlayer.pause()
        if (cmd == 'seek_up'):
            app.radioTunerTh.next()
        if (cmd == 'seek_down'):
            app.radioTunerTh.previous()
        if (cmd == 'turn_on'):
            if app.radioTunerTh.radioTuner.on == False:
                app.radioTunerTh.tune(97.2)
            app.radioTunerTh.play()
        if (cmd == 'turn_off'):
            app.radioTunerTh.pause()


    @app.webserverTh.flaskApp.route('/set-radio-tune', methods=['GET'])
    def setRadioTune():
        try:
            # Get arguments
            freq = float(flask_request.args.get('freq'))
            app.spotifyPlayer.pause()
            app.radioTunerTh.tune(freq)
            app.radioTunerTh.play()
            return prettyJson({'status' : 'Tuning ' + str(freq) + '!'})
        except Exception as e:
            print(e)
            return 'Invalid freq to tune'




