# About

This project is designed for long term lighting installations, specifically focussed around LED pixel strips (e.g. any 5050 strip like WS2811, WS2812B, 2812Eco, WS2813, WS2815, SK6812, SK9822), ideally making it easy to update the content.

The project is built in Python, using the [sACN module](https://github.com/Hundemeier/sacn), recordings will be stored as JSON and there will be a web GUI.

The aims of this project are to allow:
- recording of incoming E1.31 sACN data
- playback of stored recording via sACN (and possibly SPI)
- playback of videos/images with mapping of RGB(W)

View the [dev board](https://github.com/garethnunns/PixelPlayback/projects/1) to see how progress is going on these ambitions.

# Dev

This project is currently under active development (unless I've forgot to update this, in which case it no longer is).

Install Python & Pip if not already installed.

Then install the following dependencies, as defined in the [Pipfile](./Pipfile).

Module | Purpose
--- | ---
[sacn](https://pypi.org/project/sacn/) | Recording and playback
[netifaces](https://pypi.org/project/netifaces/) | Getting connected network interfaces
[opencv-python](https://pypi.org/project/opencv-python/) | Converting videos to pixels
[pyserial](https://pypi.org/project/pyserial/) | Reading power from PZEM

Install with pipenv:
````bash
pip3 install pipenv
pipenv install
````

Otherwise:
````bash
pip3 install sacn netifaces opencv-python pyserial
````

All code is linted with pylint and in the root is a .pylintrc file defining the standards.

At some point I'll remove the Node out when it's all implemented in Python.

# Pi

## Install

1. [Install Raspberry Pi OS Lite](https://www.raspberrypi.org/documentation/installation/installing-images/) and [enable SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/).

2. Once connected go into the config:

````bash
sudo raspi-config
````

- Go to **Advanced Options > Expanded Filesystem** and enable

- Go to **Interfacing Options > 1-Wire** and **Yes**

- Reboot

3. Update and upgrade any existing packages

````bash
sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade
````

4. Install Pip for Python packages management
````bash
sudo apt install -y python3-pip
````

5. [Install a load of bits needed for OpenCV](https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/)

    _Only install these if you intend to do video conversion on the Pi, it seems quite excessive..._

````bash
# Developer tools
sudo apt-get install -y build-essential cmake pkg-config

# Image & video I/O packages
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev

# GTK library
sudo apt-get install -y libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev

# Optimisations
sudo apt-get install -y libatlas-base-dev gfortran

# Other bits
sudo apt-get install -y libilmbase-dev libopenexr-dev libgstreamer1.0-dev

# It is left as a task to the reader to work out if all of that's needed...
````

6. Enable temperature probe modules (DS18B20)

````bash
sudo modprobe w1-gpio
sudo modprobe w1-therm
sudo nano /etc/modules

# then add the following lines
w1_gpio
w1_therm
# exit and save

# then likely reboot
sudo reboot
````

## DDNS

In order to access your Pi from anywhere, you will likely need to setup some for of DDNS, I quite like duckdns.org, so here are some [abridged instructions](https://www.wundertech.net/how-to-setup-duckdns-on-a-raspberry-pi/):

````bash
mkdir duckdns
cd duckdns
nano duck.sh

# edit this line to include your credentials
echo url="https://www.duckdns.org/update?domains=[YOUR_DOMAIN]&token=[YOUR_TOKEN]&ip=" | curl -k -o ~/duckdns/duck.log -K -
# exit & save

chmod 700 duck.sh
crontab -e

# add the following line
*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
# exit & save

# test run it
./duck.sh
# confirm it has run successfully
cat duck.log
sudo service cron start
````

You will then likely need to configure port forwarding in your router to allow the traffic you require, likely these ports:
- 22: SSH
- 80: HTTP
- 443: HTTPS

The exact configuration of these will depend on your router.

## Pixel Playback

Install as per the [dev instructions above](#dev) - there may be a release in future.