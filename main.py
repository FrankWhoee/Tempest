from __future__ import print_function

import datetime
import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()
import os
from os import path
import discord
import json

client = discord.Client()
data = None
SCOPES = ['https://www.googleapis.com/auth/calendar']

def save():
    with open('database.json', 'w') as outfile:
        json.dump(data, outfile)

def modify(*args):
    curr = data[args[0]]
    for i in range(1,len(args) - 2):
        curr = curr[args[i]]
    curr[data[args[-2]]] = data[args[-1]]
    save()

if path.exists("database.json"):
    with open('database.json', 'r') as f:
        data = json.load(f)
else:
    data = {}
    save()


creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('calendar', 'v3', credentials=creds)
except HttpError as error:
    print('An error occurred: %s' % error)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return


    if str(message.guild.id) in list(data.keys()) and message.channel.id == data[str(message.guild.id)]["channel"]:
        if  message.content.endswith("@gmail.com"):
            try:
                rule = {
                    'scope': {
                        'type': 'user',
                        'value': message.content,
                    },
                    'role': 'writer'
                }

                created_rule = service.acl().insert(calendarId=data[str(message.guild.id)]["cal"], body=rule).execute()
                confirmation = await message.channel.send("Shared to email.")
                time.sleep(3)
                await confirmation.delete()
                await message.delete()
            except HttpError as error:
                print('An error occurred: %s' % error)
                errormsg = await message.channel.send("Something went wrong adding your gmail. Only send your gmail into this channel.")
                time.sleep(5)
                await errormsg.delete()

        else:
            await message.delete()


    if message.content.startswith('-'):
        command = message.content[1:].split(" ")[0]
        param = message.content[1:].split(" ")[1:]
        if command == "register":
            if len(param) != 1:
                await message.channel.send("Usage: `-register CALENDARID`")
                return
            data[str(message.guild.id)] = {'channel':message.channel.id, 'cal':param[0]}
            save()
            confirmation = await message.channel.send("Channel registered for email subscription.")
            time.sleep(3)
            await confirmation.delete()
            await message.delete()
            calendar = service.calendars().get(calendarId=param[0]).execute()
            await message.channel.send("Send your gmail address into this channel to have " + calendar['summary'] + " shared with you. All messages posted to this channel will be deleted.\nExample: gonzalo@gmail.com")



client.run(os.getenv("DISCORD"))

# If modifying these scopes, delete the file token.json.
