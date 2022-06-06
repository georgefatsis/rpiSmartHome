# Smart Home Controlled from Telegram

## Description of the project
This project created to manage a smart home application using the telegram platform.

The main idea behind this project is to use a telegram bot to manage a smart home application.
We selected the telegram platform because it is an easy to access and use application that allows you to
create and manage a bot.
The application was developed in python, and it runs on a Raspberry Pi which
allows you to easily connect a series of a sensors and devices that the user will interact with using the telegram bot.

In this project the following devices used:
* RPI Camera
* PIR motion sensor
* DHT 22
* 4 relays

The code allows the user to send specific commands that will trigger specific actions in the RPI.

The commands are the following:
* /live - Check if bot is active
* /showphotos - Show the saved photos
* /showvideos - Show the saved videos
* /coffeeon - Turn on the coffee maker
* /coffeeoff - Turn of the coffee maker
* /lightson - Turn the lights on
* /lightsoff - Turn the lights off
* /heatingon - Turn the heating on
* /heatingoff - Turn the heating off
* /shadesdown - Down the shades
* /shadesup - Retreat the shades
* /piron - Turn on the PIR sensor
* /piroff - Turn off the PIR sensor
* /temperature - Check the temperature
* /humidity - Check the humidity
* /photo - Take and send a photo
* /video - Take and send a 10sec video
* /check - Checking the status of the devices
* /help - Show help

## Prerequisites

To execute the code properly please install the following:
   * sudo apt update
   * sudo apt upgrade -y
   * sudo apt install python-is-python3
   * sudo apt-get install python3-pip
   * sudo pip3 install adafruit-circuitpython-dht
   * sudo apt-get install libgpiod2
   * sudo pip3 install gpiozero
   * sudo pip install telepot
Also, enable the camera from:
   * sudo raspi-config
Create two directories under the home of the pi user:
   * mkdir /home/pi/RPIPhotos
   * mkdir /home/pi/RPIVideos

To enable the code executed each time the rpi reboots add the following entry in the
crontab of the pi user:

```
# Crontab entry for smart home:
@reboot python /home/pi/rpiSmartHome/telegrambot.py
```

## Pin Assignments:

The following pins used for each device:
   * Pin for Relay1: 17
   * Pin for Relay2: 23
   * Pin for Relay3: 24
   * Pin for Relay4: 21
   * Pin for PIR Sensor: 19
   * Pin for DHT 22: 4
