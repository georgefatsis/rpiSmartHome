#! /usr/bin/env python
################################## Python Smart Home code ##########################################
# Python script name: telegrambot.py
#
# Description:
#   This script is used to run a smart home application in RPI. The smart home is managed through
#   a telegram bot. The telegram bot supports the following commands from the user:
#       * Find out if the application is running is live.
#       * To list the latest photos that the RPI took from its camera.
#       * To list the latest videos that the RPI took from its camera.
#       * To turn on/off the coffee maker.
#       * To turn on/off the lights.
#       * To turn on/off the heating.
#       * To turn on/off the shades.
#       * To get a photo/video from the RPI camera.
#       * To enable or disable the security of the house based on the PIR sensor.
#       * To get info for the humidity and the temperature of the house.
#   The application requires the following hardware connected to the RPI:
#       * RPI Camera
#       * PIR motion sensor
#       * DHT 22
#       * 4 relays
#   Also, a Telegram bot needs to be created and its token needs to be added in the line: 345
#   To secure the application because the Telegram bot is public there is a need to add the unique
#   User ids that will have access to execute the commands in the smart home. To get the unique ids
#   Execute the code named: GetTelegramUserID.py under the same repository and add the tokens at the
#   line: 104. The following 3 sections includes information regarding the needed software
#   installation in the Raspberry Pi, and the pin assignments.
#
####################################################################################################
#
# Prerequisites:
#   To execute the following code properly please install the following:
#       * sudo apt update
#       * sudo apt upgrade -y
#       * sudo apt install python-is-python3
#       * sudo apt-get install python3-pip
#       * sudo pip3 install adafruit-circuitpython-dht
#       * sudo apt-get install libgpiod2
#       * sudo pip3 install gpiozero
#       * sudo pip install telepot
#   And also enable the camera from:
#       * sudo raspi-config
#   Create two directories under the home of the pi user:
#       * mkdir /home/pi/RPIPhotos
#       * mkdir /home/pi/RPIVideos
#
####################################################################################################
#
# Start when the RPI is booting:
#   To autostart the bot when the RPI is rebooting please do the following:
#       * crontab -e
#   And paste the following in the editor:
#       * # Crontab entry for smart home:
#       * @reboot python /home/pi/rpiSmartHome/telegrambot.py
#
####################################################################################################
#
# Pin Assignments:
#   The following pins are used for each device:
#     * Pin for Relay1: 17
#     * Pin for Relay2: 23
#     * Pin for Relay3: 24
#     * Pin for Relay4: 21
#     * Pin for PIR Sensor: 19
#     * Pin for DHT 22: 4
#
####################################################################################################

# Load the required libraries
import sys
import time
import telepot
import RPi.GPIO as GPIO
import os
import subprocess
import board
import adafruit_dht
import json
from picamera import PiCamera
from gpiozero import MotionSensor
from tkinter import PhotoImage
from turtle import onclick
from datetime import datetime

# Setup the home directory of the user
path=os.getenv("HOME")

# Setup the mode of the board
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

# Variable to pins assignment
CoffeeMaker = 17
Lights = 23
Heating = 24
Shades = 21
pir = MotionSensor(19)

# Initialize the DHT22 device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(4)

# Initialize the tuple for the Listener.
chat_listen = {}
# TODO: Add in the line below the user IDs that will be able to execute commands in the bot.
userIDs = {}

# Setup the output pins
GPIO.setup(CoffeeMaker, GPIO.OUT)
GPIO.setup(Lights, GPIO.OUT)
GPIO.setup(Heating, GPIO.OUT)
GPIO.setup(Shades, GPIO.OUT)

# Set initial status to High for the relay
GPIO.output(CoffeeMaker,GPIO.HIGH)
GPIO.output(Lights,GPIO.HIGH)
GPIO.output(Heating,GPIO.HIGH)
GPIO.output(Shades,GPIO.HIGH)

# Function to take and send a photo to back to the bot.
def Photo(chat_id):
    bot.sendMessage (chat_id, str("Taking Photo"))
    timestr = time.strftime("%Y%m%d%H%M%S")
    # Initialize the camera
    camera = PiCamera()
    camera.start_preview()
    # Set the path to save the photo file
    folderName='/RPIPhotos'
    fileTime= folderName + '/pic' + timestr + '.jpg'
    # Capture the photo
    camera.capture(path + fileTime ,resize=(640,480))
    time.sleep(2)
    # Stop recording and close the camera module.
    camera.stop_preview()
    camera.close()
    # Seding picture
    bot.sendPhoto(chat_id, photo = open(path + fileTime, 'rb'))

# Function to send a video back to the bot.
def Video(chat_id):
    bot.sendMessage (chat_id, str("Taking a 10sec video"))
    timestr = time.strftime("%Y%m%d%H%M%S")
    # Initialize the camera
    camera = PiCamera()
    camera.resolution = (640, 480)
    # Set the path to save the video file
    folderName='/RPIVideos'
    fileTime= folderName + '/Video' + timestr + '.h264'
    # Start the recording for 10 seconds
    camera.start_recording(path + fileTime)
    camera.wait_recording(10)
    # Stop the recording and close the camera module.
    camera.stop_recording()
    camera.close()
    # Send the video
    bot.sendVideo(chat_id, video = open(path + fileTime, 'rb'))

# Function that handles the inbound messages
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    # Get the unique identifier of the user.

    userJson=json.dumps(bot.getChat(chat_id))
    userID=json.loads(userJson)['id']
    print("%s", userJson)
    userName=json.loads(userJson)['first_name']

# Execute the commands only for the authenticated usersIDs.
    if userID in userIDs:
        # Read the commands of the authenticated users.
        bot.sendMessage (chat_id,str("The user: %s is authenticated" % userName))
        # Reply to message if the python code is running
        if command == '/live':
            bot.sendMessage (chat_id, str("Hi! RPI is Ready"))
        # Replies with the photos included in the directory RPIPhotos
        elif command == '/showphotos':
            stream = os.popen('ls -1rt /home/pi/RPIPhotos')
            output = stream.read()
            bot.sendMessage(chat_id, str("%s" % output))
        # Replies with the videos included in the directory RPIVideos
        elif command == '/showvideos':
            stream = os.popen('ls -1rt /home/pi/RPIVideos')
            output = stream.read()
            bot.sendMessage(chat_id, str("%s" % output))
        # Enables the coffeemaker and replies to the user
        elif command =='/coffeeon':
           channel_is_on = GPIO.input(CoffeeMaker)
           if channel_is_on:
             GPIO.output(CoffeeMaker, GPIO.LOW)
             bot.sendMessage(chat_id, str("Coffee maker is warming"))
           else:
             bot.sendMessage(chat_id, str("Coffee maker is already on"))
        # Deactivates the coffeemaker and replies to the user
        elif command =='/coffeeoff':
           bot.sendMessage(chat_id, str("Starting the Coffee maker"))
           GPIO.output(CoffeeMaker, GPIO.HIGH)
           bot.sendMessage(chat_id, str("Coffee maker is warming"))
        # Turns the lights on and replies to the user
        elif command =='/lightson':
           channel_is_on = GPIO.input(Lights)
           if channel_is_on:
             GPIO.output(Lights, GPIO.LOW)
             bot.sendMessage(chat_id, str("The lights are on"))
           else:
             bot.sendMessage(chat_id, str("The lights are already on"))
        # Turns the lights off and replies to the user
        elif command =='/lightsoff':
           bot.sendMessage(chat_id, str("Turning off the Lights"))
           GPIO.output(Lights, GPIO.HIGH)
           bot.sendMessage(chat_id, str("The lights are off"))
        # Turns the heating on if the temperature is lower or equal to 24oC
        elif command =='/heatingon':
           channel_is_on = GPIO.input(Heating)
           temperature_c = dhtDevice.temperature
           if temperature_c <= 24:
                if channel_is_on:
                  GPIO.output(Heating, GPIO.LOW)
                  bot.sendMessage(chat_id, str("Turning on the Heating"))
                else:
                  bot.sendMessage(chat_id, str("The heating is on"))
           else:
                bot.sendMessage(chat_id, str("Temperature is %s and it is above 24oC so the heating won't turn  on" %temperature_c))
        # Turns the heating off and replies to the user
        elif command =='/heatingoff':
           bot.sendMessage(chat_id, str("Turning off the heating"))
           GPIO.output(Heating, GPIO.HIGH)
           bot.sendMessage(chat_id, str("The heating is off"))
        # Lowering the shades and  replies to the user
        elif command =='/shadesdown':
           channel_is_on = GPIO.input(Shades)
           if channel_is_on:
             GPIO.output(Shades, GPIO.LOW)
             bot.sendMessage(chat_id, str("Lowering the shades"))
             time.sleep(20)
             GPIO.output(Shades, GPIO.HIGH)
             bot.sendMessage(chat_id, str("The shades are down"))
           else:
             bot.sendMessage(chat_id, str("Shades are already down"))
        # Retracting the shades and replies to the user
        elif command =='/shadesup':
           channel_is_on = GPIO.input(Shades)
           if channel_is_on:
             GPIO.output(Shades, GPIO.LOW)
             bot.sendMessage(chat_id, str("The shades are retracting"))
             time.sleep(20)
             GPIO.output(Shades, GPIO.HIGH)
             bot.sendMessage(chat_id, str("The shades are up"))
           else:
             bot.sendMessage(chat_id, str("Shades are already down"))
        # Enables the PIR monitoring and informs the user in case there is motion
        elif command =='/piron':
            if chat_id not in chat_listen:
                chat_listen[chat_id] = True
                bot.sendMessage(chat_id, "Started Listen Motion")
            elif chat_listen[chat_id]:
                bot.sendMessage(chat_id, "Already Listening")
            else:
                chat_listen[chat_id] = True
                bot.sendMessage(chat_id, "Restarted Listen Motion")
        # Deactivates the PIR monitoring and informs the user
        elif command =='/piroff':
            if chat_id not in chat_listen:
                chat_listen[chat_id] = False
                bot.sendMessage(chat_id, "Wasn't Listening Motion")
            elif chat_listen[chat_id]:
                chat_listen[chat_id] = False
                bot.sendMessage(chat_id, "Stopped Listening")
            else:
                bot.sendMessage(chat_id, "Wasn't Listen Motion")
        # Collecting the temperature of the room and replies to the user with the temperature
        elif command =='/temperature':
           temperature_c = dhtDevice.temperature
           bot.sendMessage(chat_id, str("Temperature= %s C" % temperature_c))
        # Collecting the humidity of the room and replies to the user with the humidity
        elif command =='/humidity':
           humidity = dhtDevice.humidity
           bot.sendMessage(chat_id, str("The humidity is: {} %".format(humidity)))
        # Takes photo and sends to the user
        elif command =='/photo':
           Photo(chat_id)
        # Takes video and sends to the user
        elif command =='/video':
           Video(chat_id)
        # Checks the status of the devices and replies to the user
        elif command =='/check':
           pins = [CoffeeMaker, Lights, Heating, Shades]
           for x in pins:
             if x==CoffeeMaker:
                 pin_name='Coffee Maker'
             elif x==Lights:
                 pin_name='Lights'
             elif x==Heating:
                 pin_name='Heating'
             elif x==Shades:
                 pin_name='Shades'
             channel_is_on = GPIO.input(x)
             if channel_is_on:
                bot.sendMessage(chat_id, str("Device %s is Off" % pin_name))
             else:
                bot.sendMessage(chat_id, str("Device %s is On" % pin_name))
        # Help command for all the available commands
        elif command =='/help':
            bot.sendMessage (chat_id, str('''The following commands are available:
* /live
* /showphotos
* /showvideos
* /coffeeon
* /coffeeoff
* /lightson
* /lightsoff
* /heatingon
* /heatingoff
* /shadesdown
* /shadesup
* /photo
* /video
* /piron
* /piroff
* /temperature
* /humidity
* /help '''))

        else:
            # In case the command is not included in the acceptable commands replies to the user
            bot.sendMessage (chat_id, str("No command found. Please use /help command for help"))
    else:
        # Send a rejection message for the authenticated user.
        bot.sendMessage (chat_id,str("The user: %s is not authenticated" % userName))


# Functions used in case the PIR sensor is on and the user wants notification.
def notify_motion():
   for chat_id, listening in chat_listen.items():
      notify("Motion Detected")
      Photo(chat_id)
# Replies to the user in case the PIR sensor was activated and the user wants notification
def notify(msg):
    for chat_id, listening in chat_listen.items():
        if listening:
            bot.sendMessage(chat_id, msg)
# Monitors the PIR sensor when there is motion calls the function notify_motion
pir.when_motion = notify_motion

# Setup of the Telegram bot details
# TODO: replace <TOKEN> with the Token of your telegram bot.
bot = telepot.Bot('<TOKEN>')
bot.message_loop(handle)
print('I am listening...')

# Main loop
while 1:
    try:
        time.sleep(10)

    except KeyboardInterrupt:
        print('\n Program interrupted')
        GPIO.cleanup()
        exit()

    except:
        print('Other error or exception occured!')
        GPIO.cleanup()
