#!/bin/bash

function install_component() {
  component=$1
  echo " -> Get $component installer"
  wget -O tmp.zip "$component"
  echo ">> Install $component:"
  echo " -> Extract installer"
  unzip tmp.zip -d tmp
  cd tmp
  echo " -> Execute installer"
  source install.sh
  echo " -> Clean up"
  cd ..
  rm -rf tmp
}


#### SCRIPT EXECUTION STARTS HERE ####
echo "************************************"
echo "******* splitFlapClockRadio  *******"
echo "*******   Install/Upgrade    *******"
echo "************************************"

install_component "https://github.com/iz2k/splitFlapClockRadio/raw/master/sw/pyBackend/dist/splitFlapClockRadioBackend_1.0.zip"
install_component "https://github.com/iz2k/splitFlapClockRadio/raw/master/sw/ngFrontend/dist/splitFlapClockRadioFrontend_1.0.zip"