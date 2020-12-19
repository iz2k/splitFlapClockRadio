import os
import socket


def create_if_needed(dirPath):
    if not os.path.isdir(dirPath):
        os.mkdir(dirPath)

def get_host_info():
    hostname = socket.gethostname()
    ip = getIP()

    hostinfo =  {
        'hostname' : hostname,
        'ip' : ip
    }
    return hostinfo

def getIP():
    return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [
        [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
         [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
