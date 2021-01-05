import subprocess

from splitFlapClockRadioBackend.tools.osTools import execute


class SpotifyPlayer:

	currentTrack = 'None'

	def __init__(self):
		self.set_local_device()
		self.pause()

	def set_local_device(self):
		output=execute('/home/pi/.local/bin/spotify device -s Split-Flap-Clock-Radio')
		if len(output.splitlines())>0:
			print('[spotify] Setting Spotify device to Raspotify: ' + output.splitlines()[0])
		else:
			print('[spotify] Problem during set local device: ')


	def pause(self):
		output=execute('/home/pi/.local/bin/spotify pause')
		if len(output.splitlines())>0:
			self.currentTrack = output.splitlines()[1].lstrip()
		else:
			self.currentTrack = 'N/A'
		print('[spotify] PAUSE: ' + self.currentTrack)

	def play(self):
		output=execute('/home/pi/.local/bin/spotify play')
		if len(output.splitlines())>0:
			self.currentTrack = output.splitlines()[1].lstrip()
		else:
			self.currentTrack = 'N/A'
		print('[spotify] PLAY: ' + self.currentTrack)

	def next(self):
		output=execute('/home/pi/.local/bin/spotify next')
		if len(output.splitlines())>0:
			self.currentTrack = output.splitlines()[1].lstrip()
		else:
			self.currentTrack = 'N/A'
		print('[spotify] NEXT: ' + self.currentTrack)

	def previous(self):
		output=execute('/home/pi/.local/bin/spotify previous')
		if len(output.splitlines())>0:
			self.currentTrack = output.splitlines()[1].lstrip()
		else:
			self.currentTrack = 'N/A'
		print('[spotify] PREVIOUS: ' + self.currentTrack)
