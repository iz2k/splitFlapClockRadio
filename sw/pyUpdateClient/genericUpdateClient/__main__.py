#!/usr/bin/env python3
import argparse
import sys

from executorUpdater.backend.installThread import installThread
from executorUpdater.backend.localSwManager import localSwManager
from executorUpdater.backend.remoteSwManager import remoteSwManager
from executorUpdater.backend.webServer import define_webserver
from executorUpdater.tools.os_tools import get_host_info


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Server Side R102-tester Software repository.')

    # Optional arguments
    parser.add_argument("-pu", "--portupdater", type=int, default='8086', help="TCP listening port of the updater")
    parser.add_argument("-pr", "--portrepository", type=int, default='80', help="TCP listening port of the repository")
    parser.add_argument("-a", "--address", type=str, default='execrepos.farsens.com', help="Repository address")
    parser.add_argument("-p", "--installPath", type=str, default='/usr/share/executor', help='Sw installation path')
    return parser.parse_args()

def main(argv):
    debug=False
    args = parse_cmd_arguments()

    thInstall = installThread(debug)

    lSwManager = localSwManager(args.installPath, thInstall.queue)
    rSwManager = remoteSwManager(args.address, args.portrepository)


    # Create WebServer (without starting it)
    [app, sio] = define_webserver(debug=debug, lSwManager=lSwManager, rSwManager=rSwManager, qInstall=thInstall.queue)

    thInstall.set_sio(sio)

    try:

        # Start Install thread
        thInstall.start()

        host_info = get_host_info()

        print('Starting Web Server:')
        print('\t\thttp://' + host_info['hostname'] + ':' +  str(args.portupdater))
        print('\t\thttp://' + host_info['ip'] + ':' +  str(args.portupdater))

        # Start Webserver (blocks this thread until server quits)
        sio.run(app, port=args.portupdater, host='0.0.0.0', debug=debug)

        # When server ends, end app
        thInstall.stop()

        # Print Goodby msg
        print('Exiting Executor Updater...')

    except KeyboardInterrupt:
        thInstall.stop()

        print('Interrupted from keyboard...')

    except Exception as e:
        print(e)
        quit(0)

# If executed as main, call main
if __name__ == "__main__":
    main(sys.argv)

