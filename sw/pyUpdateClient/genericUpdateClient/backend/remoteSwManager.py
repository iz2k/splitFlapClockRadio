import cgi
import http.client
import json
import requests


class remoteSwManager:

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.url = self.address + ':' + str(self.port)

    def getLatestSwVersions(self):
        try:
            conn = http.client.HTTPConnection(self.url)
            conn.request("GET", "/get-latest")
            resp = conn.getresponse()
            data =resp.read()
            jdata = json.loads(data)
            conn.close()
            return jdata
        except Exception as e:
            print(e)
            return None

    def getComponent(self, component, version):
        try:
            fileurl = 'http://' + self.url + '/get-component?component=' + component + '&version=' +  version
            req = requests.get(fileurl)
            value, params = cgi.parse_header(req.headers['Content-Disposition'])
            filename = params['filename']
            with open(filename, 'wb') as f:
                f.write(req.content)
            return filename
        except Exception as e:
            return None
