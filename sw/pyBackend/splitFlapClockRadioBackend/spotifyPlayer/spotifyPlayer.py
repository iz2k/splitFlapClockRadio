from flask_socketio import SocketIO

from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.osTools import execute, restart_service


class SpotifyPlayer:

	currentArtist = ''
	currentTrack = ''
	isOn = False
	sio : SocketIO = None

	def __init__(self):
		self.set_local_device()
		self.pause()

	def set_sio(self, sio : SocketIO):
		self.sio = sio

	def check_local_device(self):
		output=execute('/home/pi/.local/bin/spotify device')
		if '* Split-Flap-Clock-Radio' in output:
			return True
		else:
			restart_service('raspotify')
			self.set_local_device()
			return False

	def set_local_device(self):
		output=execute('/home/pi/.local/bin/spotify device -s Split-Flap-Clock-Radio')
		if len(output.splitlines())>0:
			print('[spotify] Setting Spotify device to Raspotify: ' + output.splitlines()[0])
		else:
			print('[spotify] Problem during set local device: ')

	def play(self, uri=None):
		self.check_local_device()
		command = '/home/pi/.local/bin/spotify play'
		if (uri != None):
			command = command + ' --uri ' + uri
		output=execute(command)
		self.parse_spotify_status(output)
		print('[spotify] PLAY: ' + self.getStatus()['currentArtist'] + ' - ' + self.getStatus()['currentTrack'])

	def pause(self):
		output=execute('/home/pi/.local/bin/spotify pause')
		self.parse_spotify_status(output)
		print('[spotify] PAUSE: ' + self.getStatus()['currentArtist'] + ' - ' + self.getStatus()['currentTrack'])

	def next(self):
		output=execute('/home/pi/.local/bin/spotify next')
		self.parse_spotify_status(output)
		print('[spotify] NEXT: ' + self.getStatus()['currentArtist'] + ' - ' + self.getStatus()['currentTrack'])

	def previous(self):
		output=execute('/home/pi/.local/bin/spotify previous')
		self.parse_spotify_status(output)
		print('[spotify] PREVIOUS: ' + self.getStatus()['currentArtist'] + ' - ' + self.getStatus()['currentTrack'])

	def parse_spotify_status(self, cmdoutput):
		if len(cmdoutput.splitlines())>1:
			line1 = cmdoutput.splitlines()[0].lstrip()
			if ("Playing: " in line1):
				self.isOn = True
			if ("Paused: " in line1):
				self.isOn = False
			line2 = cmdoutput.splitlines()[1].lstrip()
			self.currentArtist = line2.split(' - ')[0]
			self.currentTrack = line2.split(' - ')[1]
		else:
			self.currentArtist = ''
			self.currentTrack = ''
			self.isOn = False

		self.emitStatus()

	def getStatus(self):
		return {
			'isOn':self.isOn,
			'currentArtist':self.currentArtist,
			'currentTrack':self.currentTrack,
		}

	def emitStatus(self):
		if self.sio != None:
			print('emitting spotifystatus')
			self.sio.emit('spotifyReport', prettyJson(self.getStatus()))
