import os
from pathlib import Path

from flask import send_file

from executorRepository.tools.json_tools import json_from_any


def define_webserver(debug, repManager):
    if debug == False:
        import eventlet

        # Monkey_Patch eventlet to support threads
        #eventlet.monkey_patch()

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


    @app.route('/get-content', methods=['GET'])
    def get_content():
        return json_from_any(repManager.parse_repository())

    @app.route('/get-latest', methods=['GET'])
    def get_latest():
        return json_from_any(repManager.get_latest())

    # /get-component?component=xxxx&version=yyy, where yyy can be version or latest
    @app.route('/get-component', methods=['GET'])
    def get_component():
        try:
            component = request.args.get('component')
            version = request.args.get('version')
            filepath = repManager.get_component_path(component, version)
            if (filepath != None):
                return send_file(filepath, as_attachment=True)
            else:
                return 'File not found'
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    @app.route('/set-component', methods=['POST'])
    def set_component():
        return repManager.set_new_component(request.files['file'])

    # /get-component?component=xxxx&version=yyy, where yyy can be version or latest
    @app.route('/get-splash', methods=['GET'])
    def get_splash():
        try:
            return send_file(Path(os.getcwd() + '/res/splash.png'), as_attachment=False)
        except Exception as e:
            print(e)
            return 'Error'
    #####################
    # Websocket events
    #####################

    @sio.on('connect')
    def onconnect_event():
        print('Client connected!')

    @sio.on('disconnect')
    def ondisconnect_event():
        print('Client disconnected!')


    return [app, sio]
