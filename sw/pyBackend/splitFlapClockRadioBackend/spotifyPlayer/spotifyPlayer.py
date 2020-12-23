import subprocess

from splitFlapClockRadioBackend.tools.osTools import execute


class SpotifyPlayer:

	currentTrack = 'None'

	def __init__(self):
		self.set_local_device()
		self.pause()

	def set_local_device(self):
		output=execute('/home/pi/.local/bin/spotify device -s Split-Flap-Clock-Radio')
		print('[spotify] Setting Spotify device to Raspotify: ' + output.splitlines()[0])

	def pause(self):
		output=execute('/home/pi/.local/bin/spotify pause')
		self.currentTrack = output.splitlines()[1].lstrip()
		print('[spotify] PAUSE: ' + self.currentTrack)

	def play(self):
		output=execute('/home/pi/.local/bin/spotify play')
		self.currentTrack = output.splitlines()[1].lstrip()
		print('[spotify] PLAY: ' + self.currentTrack)

	def next(self):
		output=execute('/home/pi/.local/bin/spotify next')
		self.currentTrack = output.splitlines()[1].lstrip()
		print('[spotify] NEXT: ' + self.currentTrack)

	def previous(self):
		output=execute('/home/pi/.local/bin/spotify previous')
		self.currentTrack = output.splitlines()[1].lstrip()
		print('[spotify] PREVIOUS: ' + self.currentTrack)
