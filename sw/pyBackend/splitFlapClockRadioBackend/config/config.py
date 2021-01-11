from splitFlapClockRadioBackend.tools.jsonTools import writeJsonFile, readJsonFile, prettyJson

class Config:

    _FILENAME='cfgSplitFlapClockRadio.json'
    params = {}

    def __init__(self):
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

    def createDefaultConfig(self):
        self.params = {
            'api' : {
                'geocodeApi': '***REMOVED***',
                'openWeatherApi': '***REMOVED***',
            },
            'clock' : {
                'timeZone' : ''
            },
            'location' : {
                'location' : '',
                'latitude' : '',
                'longitude' : ''
            },
            'sensors' : {
                'baselineEco2': 34274,
                'baselineTvoc': 34723
            },
            'raspotify' : {
                'user' : '',
                'password' : ''
            },
            'spotifyItems' : [],
            'radioItems' : []
        }
        print('Creating default config.')
        self.saveConfig()
