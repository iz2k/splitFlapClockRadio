def getKeyFromValue(myDict, myValue):
    for key in myDict:
        if myDict[key] == myValue:
            return key

def getKeyFromSubitemValue(myDict, subitemKey, subitemValue):
    for key in myDict:
        if myDict[key][subitemKey] == subitemValue:
            return key
