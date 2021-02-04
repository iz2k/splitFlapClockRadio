import os
import time

from splitFlapClockRadioBackend.tools.jsonTools import prettyJson
from splitFlapClockRadioBackend.tools.osTools import execute, restart_service, executeOnPTY


class SpotifyPlayer:

	currentArtist = ''
	currentTrack = ''
	isOn = False
	authProcess = None
	authProcessMaster = None

	def __init__(self, app):
		from splitFlapClockRadioBackend.__main__ import App
		self.app: App = app
		self.set_local_device()
		self.pause()

		from splitFlapClockRadioBackend.spotifyPlayer.spotifyPlayerWebRoutes import defineSpotifyPlayerWebRoutes
		defineSpotifyPlayerWebRoutes(self.app)

	def check_local_device(self):
		if self.app.osInfo.report['internet'] == True:
			output=execute('/home/pi/.local/bin/spotify device')
			if '* Split-Flap-Clock-Radio' in output:
				return True
			else:
				restart_service('raspotify')
				time.sleep(3)
				self.set_local_device()
				return False
		else:
			print('[spotify] No internet connection')

	def set_local_device(self):
		if self.app.osInfo.report['internet'] == True:
			output=execute('/home/pi/.local/bin/spotify device -s Split-Flap-Clock-Radio')
			if len(output.splitlines())>0:
				print('[spotify] Setting Spotify device to Raspotify: ' + output.splitlines()[0])
			else:
				print('[spotify] Problem during set local device: ')
		else:
			print('[spotify] No internet connection')

	def play(self, uri=None):
		if self.app.osInfo.report['internet'] == True:
			self.check_local_device()
			command = '/home/pi/.local/bin/spotify play'
			if (uri != None):
				command = command + ' --uri ' + uri
			output=execute(command)
			self.parse_spotify_status(output)
			print('[spotify] PLAY: ' + self.getStatus()['currentArtist'] + ' - ' + self.getStatus()['currentTrack'])
			return self.getStatus()
		else:
			print('[spotify] No internet connection')

	def pause(self):
		if self.app.osInfo.report['internet'] == True:
			output=execute('/home/pi/.local/bin/spotify pause')
			self.parse_spotify_status(output)
			print('[spotify] STOP')
		else:
			print('[spotify] No internet connection')

	def next(self):
		if self.app.osInfo.report['internet'] == True:
			output=execute('/home/pi/.local/bin/spotify next')
			self.parse_spotify_status(output)
			print('[spotify] NEXT: ' + self.getStatus()['currentArtist'] + ' - ' + self.getStatus()['currentTrack'])
		else:
			print('[spotify] No internet connection')

	def previous(self):
		if self.app.osInfo.report['internet'] == True:
			output=execute('/home/pi/.local/bin/spotify previous')
			self.parse_spotify_status(output)
			print('[spotify] PREVIOUS: ' + self.getStatus()['currentArtist'] + ' - ' + self.getStatus()['currentTrack'])
		else:
			print('[spotify] No internet connection')

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
		try:
			self.app.webserver.sio.emit('spotifyReport', prettyJson(self.getStatus()))
		except:
			pass

	def searchSpotify(self, type, terms):
		if self.app.osInfo.report['internet'] == True:
			return execute('/home/pi/.local/bin/spotify search ' + terms + ' --' + type + ' --raw')
		else:
			print('[spotify] No internet connection')
			return {}

	def getAuth(self):
		if self.app.osInfo.report['internet'] == True:
			output=execute('/home/pi/.local/bin/spotify auth status')
			if (output == ''):
				output = 'Not logged in.'
			return {
				'status': output,
			}
		else:
			print('[spotify] No internet connection')
			return {
				'status': 'No internet connection',
			}

	def startAuthProcess(self):
		if self.app.osInfo.report['internet'] == True:
			if self.authProcess is not None:
				print("[spotify] Killing Previous Auth Process")
				self.authProcess.terminate()
				self.authProcess.wait()

			cmd = '/home/pi/.local/bin/spotify auth login'

			print('[spotify] Start Auth Process')
			[self.authProcess, self.authProcessMaster] = executeOnPTY(cmd)

			time.sleep(0.1)
			x = os.read(self.authProcessMaster, 1026).decode('utf-8')
			if (x.find('\r\n\r\n') > 0):
				print('[Spotify] Auth: Get authorization URL')

				# Proceed
				os.write(self.authProcessMaster, '\n'.encode('utf-8'))

				# Wait and read response
				time.sleep(0.1)
				x = os.read(self.authProcessMaster, 1026).decode('utf-8')
				if (x.find('Please select which additional features you want to authorize') > 0):
					# Proceed with defaults
					os.write(self.authProcessMaster, 'Y\n'.encode('utf-8'))

					# Wait and read response
					time.sleep(0.1)
					x = os.read(self.authProcessMaster, 1026)
					ans = x.decode('utf-8')
					# Search URL
					idx_start = ans.find('\r\n\r\n\thttps://')
					idx_end = ans.find('\r\n\r\nEnter verification code')
					if idx_start > 0 and idx_end > 0:
						url = ans[idx_start + 5:idx_end]
						print('[Spotify] Auth URL: ' + url)
						return url
					else:
						print('[Spotify] Auth: Error parsing URL')
				else:
					print('[Spotify] Auth Process Error')
			else:
				print('[Spotify] Auth Process Error')
		else:
			print('[spotify] No internet connection')
			return 'no-internet-connection'



	def endAuthProcess(self, verificationCode):
		if self.app.osInfo.report['internet'] == True:
			if self.authProcess is None:
				return 'No Auth Process in curse'

			# Delete old configuration
			execute('rm /home/pi/.config/spotify-cli/credentials.json')

			# Enter Verification Code
			os.write(self.authProcessMaster, verificationCode.encode('utf-8'))
			# Proceed
			os.write(self.authProcessMaster, '\n'.encode('utf-8'))

			time.sleep(1)
			x = os.read(self.authProcessMaster, 1026)

			print("[spotify] Killing Auth Process")
			os.close(self.authProcessMaster)
			self.authProcess.terminate()
			self.authProcess.wait()
			return 'Auth Process done!'
		else:
			print('[spotify] No internet connection')
			return 'no-internet-connection'

	def updateRaspotifyCredentials(self, username, password):
		print('[spotify] Updating Raspotify Credentials')
		raspotifyConfig = open('/etc/default/raspotify', 'r')
		raspotifyConfigOrig = raspotifyConfig.readlines()
		raspotifyConfig = open('/etc/default/raspotify', 'w')
		for line in raspotifyConfigOrig:
			if 'OPTIONS' in line:
				raspotifyConfig.write('OPTIONS="--username ' + username + ' --password ' + password + '"\r\n')
			else:
				raspotifyConfig.write(line)
		raspotifyConfig.close()

		restart_service('raspotify')
		time.sleep(3)
		self.set_local_device()
		return 'Done'
