#!/bin/bash

function update_apt() {
  echo ">> Update APT"
  sudo apt-get update
}

function install_pigpio() {
  echo ">> Install PiGPIO:"
  sudo apt-get -y install pigpio
echo " -> Configuring pigpiod service"

cat <<EOF | sudo tee /lib/systemd/system/pigpiod.service
[Unit]
Description=Daemon required to control GPIO pins via pigpio
[Service]
ExecStart=/usr/bin/pigpiod -t 0
ExecStop=/bin/systemctl kill pigpiod
Type=forking
[Install]
WantedBy=multi-user.target
EOF

echo " -> Reloading systemctl service daemons."
sudo systemctl daemon-reload

echo " -> Enabling PiGPIO service."
sudo systemctl enable pigpiod.service
sudo systemctl start pigpiod.service
}

function install_mariaDb() {
  echo ">> Install DB:"
  echo " -> Install Maria DB"
  sudo apt-get -y install mariadb-server
  echo " -> Create DB user"
cat <<EOF | sudo mysql -u root | grep donotshowanythinginbash
CREATE USER pi;
GRANT ALL PRIVILEGES ON *.* TO 'pi'@'%' IDENTIFIED BY 'raspberry' WITH GRANT OPTION;
EOF

echo " -> Open DB to remote connections"
sudo sed -i '/bind-address            = 127.0.0.1/c\bind-address            = 0.0.0.0' /etc/mysql/mariadb.conf.d/50-server.cnf

}

function install_tools() {
  echo ">> Install Tools:"
  echo " -> Install i2c tools"
  sudo apt-get -y install i2c-tools
  echo " -> Install system tools"
  sudo apt-get -y install mmv unzip
  echo " -> Install development tools"
  sudo apt-get -y install patch xsltproc gcc libreadline-dev python3-venv python3-pip python3-pil libopenjp2-7
}

function install_raspotify() {
  echo ">> Install Raspotify:"
  curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
}

function install_spotifycli() {
  echo ">> Install Spotify-CLI:"
  sudo pip3 install spotify-cli
}

function install_tts() {
  echo ">> Install Pico TTS:"
  echo " -> Install non-free repository"
  wget -q https://ftp-master.debian.org/keys/release-10.asc -O- | sudo apt-key add -
  echo "deb http://deb.debian.org/debian buster non-free" | sudo tee -a /etc/apt/sources.list
  sudo apt-get update
  echo " -> Install libttspico"
  sudo apt-get -y install libttspico-utils
}

function install_latest() {
  echo ">> Install Latest components:"
  wget -O - https://raw.githubusercontent.com/iz2k/splitFlapClockRadio/master/sw/instLatest.sh | bash
}

function setup_i2s() {

	echo "   * Remove undesired configurations"
	sudo sed -i \
		-e "s/^dtparam=audio=on/#\0/" \
		-e "s/^#\(dtparam=i2s=on\)/\1/" \
		/boot/config.txt

	echo "   * Add i2s-mmap if not present"
	grep -q "dtoverlay=i2s-mmap" /boot/config.txt || \
		echo "dtoverlay=i2s-mmap" | sudo tee -a /boot/config.txt

	echo "   * Add i2s if not present"
	grep -q "dtparam=i2s=on" /boot/config.txt || \
		echo "dtparam=i2s=on" | sudo tee -a /boot/config.txt
		
	echo "   * Add dtoverlay if not present"
	grep -q "dtoverlay=googlevoicehat-soundcard" /boot/config.txt || \
		echo "dtoverlay=googlevoicehat-soundcard" | sudo tee -a /boot/config.txt

	echo "   * Configuring ALSA mixer"
cat <<EOF | sudo tee /etc/asound.conf
pcm.speaker {
	type softvol
	slave.pcm dmix
	control {
		name Master
		card 0
	}
}

pcm.mic {
	type route
	slave.pcm dsnoop
	ttable {
		0.0 1
		1.1 1
	}
}

pcm.!default {
	type asym
	playback.pcm "plug:speaker"
	capture.pcm "plug:mic"
}

ctl.!default {
	type hw
	card 0
}
EOF
}

function setup_hw() {
  echo ">> Setup HW:"
  echo " -> Enable I2C HW."
  sudo raspi-config nonint do_i2c 0

  echo " -> Enable SPI HW."
  sudo raspi-config nonint do_spi 0
  
  echo " -> Enable UART HW."
  sudo raspi-config nonint do_serial 1
  
  echo " -> Enable I2S HW."
  setup_i2s
}

function setup_hostname() {
  echo ">> Setup Hostname:"
  hostname=$1
  echo " -> Change hostname to: "$hostname
  sudo raspi-config nonint do_hostname $hostname

}

function setup_swap() {
  echo ">> Increase SWAP:"
  echo " -> Stop SWAP."
  sudo dphys-swapfile swapoff

  echo " -> Modify SWAP size in configuration file"
  sudo sed -i '/CONF_SWAPSIZE=100/c\CONF_SWAPSIZE=1024' /etc/dphys-swapfile

  echo " -> Regenerate SWAP."
  sudo dphys-swapfile setup

  echo " -> Restart SWAP."
  sudo dphys-swapfile swapon
}

function install_component() {
  component=$1
  echo ">> Install $component:"
  echo " -> Extract installer"
  unzip $component -d tmp
  cd tmp
  echo " -> Execute installer"
  source install.sh
  echo " -> Clean up"
  cd ..
  rm -rf tmp
}

function install_audio_pipe_service() {
	echo ">> Install I2S PiPe Service:"
	echo " -> Create directory"
	sudo mkdir /usr/share/iz2k
	sudo mkdir /usr/share/iz2k/i2spipe
	echo " -> Create stream script"
	
cat <<EOF | sudo tee /usr/share/iz2k/i2spipe/stream.sh
#!/usr/bin/env bash
arecord -c2 -r 48000 -f S32_LE -t wav -V stereo | aplay
EOF

	echo " -> Create Audio Pipe Service"
cat <<EOF | sudo tee /etc/systemd/system/audio-pipe.service
[Unit]
Description=Audio Pipe

[Service]
ExecStart=bash /usr/share/iz2k/i2spipe/stream.sh
WorkingDirectory=/usr/share/iz2k/i2spipe
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root
 
[Install]
WantedBy=multi-user.target
EOF

echo " -> Reloading systemctl service daemons."
sudo systemctl daemon-reload

echo " -> Enabling Audio Pipe service."
sudo systemctl enable audio-pipe.service
sudo systemctl start audio-pipe.service
}

#### SCRIPT EXECUTION STARTS HERE ####
echo "*********************************************"
echo "******* splitFlapClockRadio INSTALLER *******"
echo "*********************************************"
echo "** This script will convert a clean image  **"
echo "** of Raspberry Pi OS Lite to a working    **"
echo "** splitFlapClockRadio. This includes      **"
echo "** setting up hardware, firmware and       **"
echo "** software components.                    **"
echo "*********************************************"
echo "*********************************************"
echo "** The install is automated. All options   **"
echo "** needed for the process are requested    **"
echo "** in the beggining. A reboot is needed    **"
echo "** to finalize the process.                **"
echo "*********************************************"

read -p "Hostname will be changed in the end of the process. Select new hostname: " hostname  <&1

update_apt
install_pigpio
install_mariaDb
install_tools
install_spotifycli
install_raspotify
install_tts
setup_hw
setup_swap
install_audio_pipe_service
install_latest
setup_hostname $hostname

echo "********************************************"
echo "**** EXECUTOR SYSTEM BAREBONE INSTALLED ****"
echo "********************************************"
read -n1 -p "Do you want to reboot now? (y/N)" doit  <&1
echo ""
case $doit in
	y|Y) sudo reboot ;;
	*) echo "Manual system reboot required" ;;
esac