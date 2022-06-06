#! /usr/bin/env python
##################################### GetTelegramUserID ############################################
# Python script name: GetTelegramUserID.py
#
# Description:
#   This script is used to retrieve the unique ID of each user that sends a message to the Telegram
#   bot and send it batch to the user.
#
####################################################################################################

# Load the required libraries
import sys
import time
import telepot
import json

# Function that handles the inbound messages
def handle(msg):
   chat_id = msg['chat']['id']
   command = msg['text']

   # Get the unique identifier of the user.
   userJson=json.dumps(bot.getChat(chat_id))
   userID=json.loads(userJson)['id']
   bot.sendMessage (chat_id,str("The user unique id: %s" % userID))

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
      exit()

   except:
      print('Other error or exception occured!')
