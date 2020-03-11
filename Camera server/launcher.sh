#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/2dt301 #where the script is
sudo service motion stop
sudo python3 camera.py #a commnad to run the script
cd /
