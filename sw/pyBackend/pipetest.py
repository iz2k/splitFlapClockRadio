import os
import time

from splitFlapClockRadioBackend.tools.osTools import executeOnPTY

cmd = '/home/pi/.local/bin/spotify auth login'

print('[Spotify] Auth: Start auth process')
[p, master] = executeOnPTY(cmd)

time.sleep(0.1)
x = os.read(master, 1026).decode('utf-8')
if(x.find('\r\n\r\n')>0):
    print('[Spotify] Auth: Get authorization URL')

    # Proceed
    os.write(master, '\n'.encode('utf-8'))

    # Wait and read response
    time.sleep(0.1)
    x = os.read(master, 1026).decode('utf-8')
    if(x.find('Please select which additional features you want to authorize')>0):
        # Proceed with defaults
        os.write(master, 'Y\n'.encode('utf-8'))

        # Wait and read response
        time.sleep(0.1)
        x = os.read(master, 1026)
        ans = x.decode('utf-8')
        # Search URL
        idx_start = ans.find('\r\n\r\n\thttps://')
        idx_end = ans.find('\r\n\r\nEnter verification code')
        if idx_start > 0 and idx_end > 0:
            url = ans[idx_start + 5:idx_end]
            print('[Spotify] Auth URL: ' + url)
        else:
            print('[Spotify] Auth: Error parsing URL')
    else:
        print('[Spotify] Auth Process Error')
else:
    print('[Spotify] Auth Process Error')






