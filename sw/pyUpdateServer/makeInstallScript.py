
def create_install_script(component_name, component_description, wheel_name):
    install_script = textFile('dist/install.sh')
    install_script.addLine('echo " -> Check and Stop service"')
    install_script.addLine('systemctl stop ' + component_name + '.service')
    install_script.addLine('echo " -> Check and Remove old version"')
    install_script.addLine('rm -rf /usr/share/executor/' + component_name)
    install_script.addLine('mkdir /usr/share/executor/' + component_name)
    install_script.addLine('echo " -> Create virtual environment"')
    install_script.addLine('python3 -m venv /usr/share/executor/' + component_name + '/venv')
    install_script.addLine('cp version.txt /usr/share/executor/' + component_name + '/')
    install_script.addLine('cp -r res /usr/share/executor/' + component_name + '/res')
    install_script.addLine('echo " -> Install component"')
    install_script.addLine('/usr/share/executor/' + component_name + '/venv/bin/pip install ' + wheel_name)
    install_script.addLine('echo " -> Create executable script"')
    install_script.addLine('touch /usr/share/executor/' + component_name + '/' + component_name + '.sh')
    install_script.addLine('echo "/usr/share/executor/' + component_name + '/venv/bin/python -m ' + component_name + ' \\"\$@\\"" | tee -a /usr/share/executor/' + component_name + '/' + component_name + '.sh | grep donotshowanythinginbash')
    install_script.addLine('chmod +x /usr/share/executor/' + component_name + '/' + component_name + '.sh')
    install_script.addLine('echo " -> Create symbolic link"')
    install_script.addLine('ln -f -s /usr/share/executor/' + component_name + '/' + component_name + '.sh /usr/bin/' + component_name)

    install_script.addLine('echo " -> Create ' + component_name + ' Service"')
    install_script.addLine('cat << EOF | tee /etc/systemd/system/' + component_name + '.service | grep donotshowanythinginbash')
    install_script.addLine('[Unit]')
    install_script.addLine('Description = ' + component_description)
    install_script.addLine('After = network.target')
    install_script.addLine('')
    install_script.addLine('[Service]')
    install_script.addLine('ExecStart = /usr/share/executor/' + component_name + '/venv/bin/python -m ' + component_name)
    install_script.addLine('WorkingDirectory = /usr/share/executor/' + component_name)
    install_script.addLine('StandardOutput = inherit')
    install_script.addLine('StandardError = inherit')
    install_script.addLine('Restart = always')
    install_script.addLine('User = root')
    install_script.addLine('')
    install_script.addLine('[Install]')
    install_script.addLine('WantedBy = multi-user.target')
    install_script.addLine('EOF')

    install_script.addLine('echo " -> Enable ' + component_name + ' Service"')
    install_script.addLine('systemctl daemon-reload')
    install_script.addLine('systemctl enable ' + component_name + '.service')
    install_script.addLine('systemctl start ' + component_name + '.service')

    install_script.close()

class textFile:

    def __init__(self, filename, endl = '\n'):
        self.file = open(filename, 'w+', newline=endl)
        self.endl = endl

    def addLine(self, line):
        self.file.write(line + self.endl)

    def close(self):
        self.file.close()
