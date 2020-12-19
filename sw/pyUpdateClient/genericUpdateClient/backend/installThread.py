import os
import shlex
import shutil
import subprocess
import time
from queue import Queue
from threading import Thread
from zipfile import ZipFile

from eventlet import tpool
from flask_socketio import SocketIO


class installThread(Thread):

    queue = Queue()
    sio : SocketIO = None
    installRunning = False
    stdout = None
    debug = None

    def __init__(self, debug):
        Thread.__init__(self)
        self.debug = debug

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()

    def set_sio(self, sio : SocketIO):
        self.sio = sio

    def run(self):
        # Main loop
        run_app=True
        while(run_app):
            # Check if msg in queue
            while not self.queue.empty():
                [q_msg, q_data] = self.queue.get()
                if q_msg == 'install':
                    self.installComponentFromFile(q_data, self.sio)
                if q_msg == 'quit':
                    run_app=False

            time.sleep(0.01)


    def close_fd(self):
        time.sleep(0.1)
        self.stdout.close()
        self.installRunning = False


    def installComponentFromFile(self, zipfile, sio):
        print('Extracting ' + zipfile + '...')
        sio.emit('stdout', 'Extracting ' + zipfile + '...\n\r')
        with ZipFile(zipfile, 'r') as zipObj:
            zipObj.extractall(path='tmp')
        print('Executing install.sh...')
        sio.emit('stdout', 'Executing install.sh...\n\r')
        raw_cmd = 'sh install.sh'
        cmd=shlex.split(raw_cmd)
        p=subprocess.Popen(cmd, cwd='tmp',
                            stderr=subprocess.STDOUT,
                            stdout=subprocess.PIPE)

        rBytes = bytearray()
        self.installRunning = True
        self.stdout = p.stdout
        stopping=False
        while self.installRunning == True:
            if p.poll() != None:
                if stopping==False:
                    stopping=True
                    if self.debug:
                        Thread(target=self.close_fd, args=()).start()
                    else:
                        tpool.execute(self.close_fd)

            try:
                rByte = p.stdout.read(1)
                rBytes.extend(rByte)
                if rByte == b'\n' or rByte == b'\r':
                    if rByte == b'\n':
                        rBytes.extend(b'\r')
                    line = rBytes.decode()
                    print(line, end='', flush=True)
                    sio.emit('stdout', line)
                    rBytes = bytearray()
            except:
                pass


        print('Cleaning up...')
        sio.emit('stdout', 'Cleaning up...\n\r')
        shutil.rmtree('tmp')
        os.remove(zipfile)
        print('Install finished')
        sio.emit('stdout', 'Install finished\n\r')
