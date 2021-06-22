# About

This project is designed for long term lighting installations, specifically focussed around LED pixel strips (e.g. any 5050 strip like WS2811, WS2812B, 2812Eco, WS2813, WS2815, SK6812, SK9822), ideally making it easy to update the content.

The project is built in Python, using the [sACN module](https://github.com/Hundemeier/sacn), recordings will be stored as JSON and there will be a web GUI.

The aims of this project are to allow:
- recording of incoming E1.31 sACN data
- playback of stored recording via sACN (and possibly SPI)
- playback of videos/images with mapping of RGB(W)

# Installation

Install Python if not already installed.

Then install the following dependencies:

Module | Purpose
--- | ---
[sacn](https://pypi.org/project/sacn/) | Recording and playback
[netifaces](https://pypi.org/project/netifaces/) | Getting connected network interfaces

````bash
pip3 install sacn netifaces
````