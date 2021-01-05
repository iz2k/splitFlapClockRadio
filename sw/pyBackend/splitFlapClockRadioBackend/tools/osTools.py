import os
import shutil
import subprocess

def getDiskUsage():
    stat = shutil.disk_usage(os.getcwd())
    total_GB = "%.2f" % (stat.total / 1024 / 1024 / 1024)
    free_GB = "%.2f" % (stat.free / 1024 / 1024 / 1024)
    return [total_GB, free_GB]

def check_service_running(service):
    cmd = 'systemctl is-active --quiet ' + service
    out = subprocess.run(cmd.split(), capture_output=True)
    if out.returncode == 0:
        return True
    else:
        return False

def start_service(service):
    print('Starting ' + service + ' service')
    cmd = 'sudo service ' + service + ' start'
    subprocess.run(cmd.split(), capture_output=True)

def stop_service(service):
    print('Stopping ' + service + ' service')
    cmd = 'sudo service ' + service + ' stop'
    subprocess.run(cmd.split(), capture_output=True)

def start_service_async(service):
    print('Starting ' + service + ' service')
    cmd = 'sudo service ' + service + ' start'
    subprocess.Popen(cmd.split())

def stop_service_async(service):
    print('Stopping ' + service + ' service')
    cmd = 'sudo service ' + service + ' stop'
    subprocess.Popen(cmd.split())

def execute(cmd):
    p = subprocess.Popen(cmd.split(), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    output, error = p.communicate()
    return output.decode("utf-8")
