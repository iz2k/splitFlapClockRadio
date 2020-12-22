import subprocess

class SpotifyPlayer:

	def __init__(self):
		self.set_local_device()
		self.pause()

	def set_local_device(self):
		print('[spotify] Setting Spotify device to Raspotify.')
		raw_cmd = '/home/pi/.local/bin/spotify device -s raspotify'
		subprocess.call(raw_cmd, shell=True)

	def pause(self):
		raw_cmd = '/home/pi/.local/bin/spotify pause'
		subprocess.call(raw_cmd, shell=True)

	def play(self):
		raw_cmd = '/home/pi/.local/bin/spotify play'
		subprocess.call(raw_cmd, shell=True)

	def next(self):
		raw_cmd = '/home/pi/.local/bin/spotify next'
		subprocess.call(raw_cmd, shell=True)

	def previous(self):
		raw_cmd = '/home/pi/.local/bin/spotify previous'
		subprocess.call(raw_cmd, shell=True)
