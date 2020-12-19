import time

from executorUpdater.backend.localSwManager import localSwManager
from executorUpdater.backend.remoteSwManager import remoteSwManager
from executorUpdater.tools.json_tools import json_from_any

def define_webserver(debug, lSwManager : localSwManager, rSwManager : remoteSwManager, qInstall):
    if debug == False:
        import eventlet

        # Monkey_Patch eventlet to support threads
        eventlet.monkey_patch()

    from flask import Flask, request
    from flask_socketio import SocketIO
    from flask_cors import CORS
    # Create Flask App
    app = Flask(__name__, static_folder='web', static_url_path='')
    # Enable CORS to Flask
    CORS(app)
    # Add SocketIO to app
    if debug == True:
        sio = SocketIO(app, async_mode='threading')
    else:
        sio = SocketIO(app, async_mode='eventlet')
    # Enable CORS to SocketIO
    sio.init_app(app, cors_allowed_origins="*")

    #####################
    # REST routes
    #####################


    @app.route('/check-updates', methods=['GET'])
    def checkUpdates():
        installedVersions=lSwManager.getInstalledVersions()
        remoteVersions=rSwManager.getLatestSwVersions()
        return json_from_any({'local':installedVersions,
                             'remote': remoteVersions})

    # /install-component?component=xxxx&version=yyy, where yyy can be version or latest
    @app.route('/install-component', methods=['GET'])
    def install_component():
        try:
            component = request.args.get('component')
            version = request.args.get('version')
            filename = rSwManager.getComponent(component, version)
            status = lSwManager.installComponentFromFile(filename)
            return json_from_any(status)
        except Exception as e:
            print(e)
            return 'Invalid parameters'


    #####################
    # Websocket events
    #####################

    @sio.on('connect')
    def onconnect_event():
        print('Client connected!')

    @sio.on('disconnect')
    def ondisconnect_event():
        print('Client disconnected!')

    @sio.on('handshake')
    def onhandshake_event(data):
        print(data)
        time.sleep(.1)
        sio.emit('handshake', 'Hello from Flask')


    return [app, sio]
