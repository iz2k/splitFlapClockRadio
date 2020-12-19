import os
from pathlib import Path


class localSwManager:

    def __init__(self, installPath, qInstall):
        self.path = installPath
        self.qInstall = qInstall

    def getInstalledVersions(self):
        installedComponents = []
        components = os.listdir(Path(self.path))
        for component in components:
            componentPath = Path(self.path + '/' + component)
            print(componentPath)
            version = self.getComponentVersion(componentPath)
            installedComponents.append({'component':component,
                                        'version': version})
        return installedComponents

    def getComponentVersion(self, componentPath):
        filename = Path(str(componentPath) + '/version.txt')
        if not os.path.isfile(filename):
            return None
        fo = open(filename, 'r')
        lines = fo.readlines()
        if len(lines) < 1 :
            return None
        return lines[0]

    def installComponentFromFile(self, filename):
        if filename == None:
            return {'status': 'error'}
        else:
            self.qInstall.put(['install', filename])
            return {'status': 'install triggered'}