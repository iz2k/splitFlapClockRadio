import os
import time
from queue import Queue
from threading import Thread

from splitFlapClockRadioBackend.spotifyPlayer import BIN_DIR
from splitFlapClockRadioBackend.tools.osTools import executeOnPTY, execute


class SpotipyAuth(Thread):

    queue = Queue()
    authProcess = None
    authProcessMaster = None
    url = None
    app = None

    def __init__(self, app):
        Thread.__init__(self)
        from splitFlapClockRadioBackend.__main__ import App
        self.app: App = app
        self.start()

        @self.app.webserver.sio.on('spotipy-auth')
        def spotify_event(data):
            self.handleSioEvent(data)

    def start(self):
        Thread.start(self)

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('Alarm thread exit.')

    def run(self):
        # Main loop
        run_app=True
        while(run_app):

            # Check if msg in queue
            while not self.queue.empty():
                [q_msg, q_data] = self.queue.get()
                if q_msg == 'quit':
                    run_app=False
                if q_msg == 'getURL':
                    self.url = ''
                    self.url = self.requestURL()
                if q_msg == 'setCode':
                    self.enterVerificationCode(q_data)

            time.sleep(0.1)

    def startAuthProcess(self):
        self.queue.put(['getURL', ''])

    def endAuthProcess(self, verificationCode):
        self.queue.put(['setCode', verificationCode])

    def requestURL(self):
        if self.app.osInfo.report['internet'] == True:
            if self.authProcess is not None:
                print("[spotify] Killing Previous Auth Process")
                self.authProcess.terminate()
                self.authProcess.wait()

            cmd = BIN_DIR + 'spotify auth login'

            print('[spotify] Start Auth Process')
            [self.authProcess, self.authProcessMaster] = executeOnPTY(cmd)

            time.sleep(1)
            x = os.read(self.authProcessMaster, 1026).decode('utf-8')
            if (x.find('\r\n\r\n') > 0):
                print('[Spotify] Auth: Get authorization URL')

                # Proceed
                os.write(self.authProcessMaster, '\n'.encode('utf-8'))

                # Wait and read response
                time.sleep(1)
                x = os.read(self.authProcessMaster, 1026).decode('utf-8')
                if (x.find('Please select which additional features you want to authorize') > 0):
                    # Proceed with defaults
                    os.write(self.authProcessMaster, 'Y\n'.encode('utf-8'))

                    # Wait and read response
                    time.sleep(1)
                    x = os.read(self.authProcessMaster, 1026)
                    ans = x.decode('utf-8')
                    # Search URL
                    idx_start = ans.find('\r\n\r\n\thttps://')
                    idx_end = ans.find('\r\n\r\nEnter verification code')
                    if idx_start > 0 and idx_end > 0:
                        url = ans[idx_start + 5:idx_end]
                        print('[Spotify] Auth URL: ' + url)
                        return url
        return ''


    def enterVerificationCode(self, verificationCode):
        if self.app.osInfo.report['internet'] == True:
            if self.authProcess is None:
                return 'No Auth Process in curse'

            # Delete old configuration
            execute('rm /root/.config/spotify-cli/credentials.json')

            print("[spotify] Setting Auth Code: " + verificationCode)
            # Enter Verification Code
            os.write(self.authProcessMaster, verificationCode.encode('utf-8'))
            # Proceed
            os.write(self.authProcessMaster, '\n'.encode('utf-8'))

            time.sleep(1)
            x = os.read(self.authProcessMaster, 1026)

            print("[spotify] Ending Auth Process")
            os.close(self.authProcessMaster)
            self.authProcess.terminate()
            self.authProcess.wait()
            return 'Auth Process done!'
        else:
            print('[spotify] No internet connection')
            return 'no-internet-connection'


    def handleSioEvent(self, data):
        cmd = data[0]
        arg = data[1]
        if (cmd == 'reqUrl'):
            self.app.webserver.sio.emit('spotipy-auth', ['reqUrl', self.requestURL()])
        if (cmd == 'setCode'):
            self.enterVerificationCode(arg)
            self.app.webserver.sio.emit('spotipy-auth', ['setCode', 'done'])
