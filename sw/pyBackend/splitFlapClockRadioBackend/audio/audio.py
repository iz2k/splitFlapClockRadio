import os
import wave
import shlex

import alsaaudio
import subprocess



class Audio:
    mute = False
    volume_step = 2
    say = None

    def __init__(self, app):
        from splitFlapClockRadioBackend.__main__ import App
        self.app: App = app
        self.device = alsaaudio.PCM(device='default')
        self.mixer = alsaaudio.Mixer('Master')
        self.volume = self.mixer.getvolume()[0]
        self.bindir = os.path.dirname(os.path.realpath(__file__))

        from splitFlapClockRadioBackend.audio.audioWebRoutes import defineAudioWebRoutes
        defineAudioWebRoutes(self.app)

    def play(self, wavfile):
        # Open PCM file
        f = wave.open(self.bindir + '/sounds/' + wavfile + '.wav', 'rb')

        # Set attributes
        self.device.setchannels(f.getnchannels())
        self.device.setrate(f.getframerate())

        # 8bit is unsigned in wav files
        if f.getsampwidth() == 1:
            self.device.setformat(alsaaudio.PCM_FORMAT_U8)
        # Otherwise we assume signed data, little endian
        elif f.getsampwidth() == 2:
            self.device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        elif f.getsampwidth() == 3:
            self.device.setformat(alsaaudio.PCM_FORMAT_S24_3LE)
        elif f.getsampwidth() == 4:
            self.device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
        else:
            raise ValueError('Unsupported format')

        periodsize = f.getframerate() // 8

        self.device.setperiodsize(periodsize)

        data = f.readframes(periodsize)
        while data:
            # Read data from stdin
            self.device.write(data)
            data = f.readframes(periodsize)

        f.close()

    def update_volume(self):
        if self.app.webserver.sio != None:
            self.app.webserver.sio.emit('volume', {'mute': self.mute, 'volume': self.volume})
        if self.mute is False:
            self.mixer.setvolume(self.volume)
            print('[sound] Volume:', self.volume)
        else:
            self.mixer.setvolume(0)
            print('[sound] Volume:', self.volume, '[MUTED]')

    def volume_up(self):
        retval = False
        if self.volume <= 100 - self.volume_step:
            self.volume += self.volume_step
            self.play('beep')
            retval = True
        else:
            self.play('limit')
        self.update_volume()
        return retval

    def volume_down(self):
        retval = False
        if self.volume >= self.volume_step:
            self.volume -= self.volume_step
            self.play('beep')
            retval = True
        self.update_volume()
        return retval

    def set_volume(self, vol):
        if vol >=0 and vol <=100:
            self.volume = vol
        self.update_volume()

    def toggle_mute(self):
        self.mute = not self.mute
        self.update_volume()
        return self.mute

    def say_text(self, text, lang='en', wait=False):
        raw_cmd = 'mplayer -ao alsa -af volume=3 -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob'
        raw_cmd += '&tl='
        raw_cmd += lang
        raw_cmd += '&q='
        raw_cmd += text
        raw_cmd += '"'

        cmd = shlex.split(raw_cmd)
        if wait:
            subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            if (self.say is not None):
                self.say.terminate()
                self.say.wait()
            self.say = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def say_text_offline(self, text, lang='es-ES', wait=False):
        raw_cmd = 'pico2wave -w text.wav'
        raw_cmd += ' -l ' + lang
        raw_cmd += ' "' + text + '"'

        cmd = shlex.split(raw_cmd)
        subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        raw_cmd = 'aplay text.wav'
        cmd = shlex.split(raw_cmd)
        if wait:
            subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            if (self.say is not None):
                self.say.terminate()
                self.say.wait()
            self.say = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


