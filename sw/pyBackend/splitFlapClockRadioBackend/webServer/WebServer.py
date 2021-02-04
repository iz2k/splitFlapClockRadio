import eventlet
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from queue import Queue
from threading import Thread

from splitFlapClockRadioBackend.tools.ipTools import getHostname, getIP


class WebServer(Thread):

    queue = Queue()
    sio: SocketIO = None
    flaskApp: Flask = None

    def __init__(self, app):
        Thread.__init__(self)
        from splitFlapClockRadioBackend.__main__ import App
        self.app: App = app
        eventlet.monkey_patch()

        # Create Flask App
        self.flaskApp = Flask(__name__, static_folder='web', static_url_path='')
        # Enable CORS to Flask
        CORS(self.flaskApp)
        # Add SocketIO to app
        self.sio = SocketIO(self.flaskApp, cors_allowed_origins="*", logger=False, engineio_logger=False, async_mode='eventlet')

    def start(self, port, host, debug, use_reloader):
        self.port = port
        self.host = host
        self.debug = debug
        self.use_reloader = use_reloader
        Thread.start(self)

    def stop(self):
        print('[webserver] trying to stop flask')

    def run(self):
        # When server starts, set flag
        self.isRunning = True

        # Start Webserver (blocks this thread until server quits)
        print('[webserver] Starting Web Server:')
        print('[webserver] \t\thttp://' + getHostname() + ':' + str(self.port))
        print('[webserver] \t\thttp://' + getIP() + ':' + str(self.port))
        self.sio.run(self.flaskApp, port=self.port, host=self.host, debug=self.debug, use_reloader = self.use_reloader)

        # When server ends, reset flag
        self.isRunning = False

