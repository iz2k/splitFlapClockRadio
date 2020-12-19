#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

from executorRepository.tools.os_tools import get_host_info
from executorRepository.backend.repositoryManager import repositoryManager
from executorRepository.backend.webServer import define_webserver


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Server Side R102-tester Software repository.')

    # Optional arguments
    parser.add_argument("-p", "--port", type=int, default='8085', help="TCP listening port")
    parser.add_argument("-f", "--folder", type=str, default='../resources', help="Resources folder path")
    return parser.parse_args()

def main(argv):
    debug=False
    args = parse_cmd_arguments()

    repManager = repositoryManager(Path(os.path.abspath(os.curdir) + '/' + args.folder))

    # Create WebServer (without starting it)
    [app, sio] = define_webserver(debug=debug, repManager=repManager)

    try:

        host_info = get_host_info()

        print('Starting Executor Repository Server:')
        print('\t\thttp://' + host_info['hostname'] + ':' +  str(args.port))
        print('\t\thttp://' + host_info['ip'] + ':' +  str(args.port))

        # Start Webserver (blocks this thread until server quits)
        sio.run(app, port=args.port, host='0.0.0.0', debug=debug)
    except Exception as e:
        print(e)

# If executed as main, call main
if __name__ == "__main__":
    main(sys.argv)

