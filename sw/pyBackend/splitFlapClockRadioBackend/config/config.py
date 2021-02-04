
from splitFlapClockRadioBackend.tools.jsonTools import writeJsonFile, readJsonFile, prettyJson

class Config:

    _FILENAME='cfgSplitFlapClockRadio.json'
    params = {}

    def __init__(self, app):
        from splitFlapClockRadioBackend.__main__ import App
        self.app: App = app
        self.loadConfig()

    def saveConfig(self):
        writeJsonFile(self._FILENAME, self.params)

    def loadConfig(self):
        self.params = readJsonFile(self._FILENAME)
        if self.params == {}:
            self.createDefaultConfig()

    def reloadConfig(self):
        self.loadConfig()
        self.printConfig()

    def printConfig(self):
        print('SplitFlapClockRadio configuration:')
        print(prettyJson(self.params))

    def updateApiParam(self, param, value):
        self.params['api'][param] = value
        self.saveConfig()

    def updateLocationParam(self, param, value):
        self.params['location'][param] = value
        self.saveConfig()

    def updateSensorParam(self, param, value):
        self.params['sensors'][param] = value
        self.saveConfig()

    def updateClockParam(self, param, value):
        self.params['clock'][param] = value
        self.saveConfig()

    def updateClockAlarm(self, idx, alarm):
        if (idx < len(self.params['clock']['alarms'])):
            # Update existing alarm
            self.params['clock']['alarms'][idx] = alarm
        else:
            # Append new alarm
            self.params['clock']['alarms'].append(alarm)
        self.saveConfig()

    def deleteClockAlarm(self, idx):
        del self.params['clock']['alarms'][idx]
        self.saveConfig()

    def addRadioItem(self, freq, PS):
        self.params['radioItems'].append(
            {
            'Frequency': freq,
            'Name': PS,
             })
        self.saveConfig()

    def deleteRadioItem(self, idx):
        del self.params['radioItems'][idx]
        self.saveConfig()

    def addSpotifyItem(self, type, name, uri, img):
        self.params['spotifyItems'].append(
            {
            'Type': type,
            'Name': name,
            'URI': uri,
            'Image': img,
             })
        self.saveConfig()

    def deletepotifyItem(self, idx):
        del self.params['spotifyItems'][idx]
        self.saveConfig()

    def createDefaultConfig(self):
        self.params = {
            'api' : {
                'geocodeApi': '',
                'openWeatherApi': '',
            },
            'clock' : {
                'timeZone' : 'Europe/Madrid',
                'alarms' : []
            },
            'location' : {
                'location' : '',
                'latitude' : '',
                'longitude' : ''
            },
            'sensors' : {
                'baselineEco2': 30000,
                'baselineTvoc': 30000
            },
            'spotifyItems' : [],
            'radioItems' : []
        }
        print('Creating default config.')
        self.saveConfig()
