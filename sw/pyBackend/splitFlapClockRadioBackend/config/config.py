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
        self.sgp.resetDevice()
        self.sgp.initConfig([int(self.params['baselineEco2']), int(self.params['baselineTvoc'])])

    def printConfig(self):
        print('SplitFlapClockRadio configuration:')
        print(prettyJson(self.params))

    def createDefaultConfig(self):
        self.params = {
            'api' : {
                'geocodeApi': '***REMOVED***',
                'openWeatherApi': '***REMOVED***',
            },
            'clock' : {
                'timeZone' : ''
            },
            'weatherStation' : {
                'location' : '',
                'latitude' : '',
                'longitude' : '',
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
