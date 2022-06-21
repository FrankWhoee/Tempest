import datetime
import os.path
from random import random
import time
import wcag_contrast_ratio as contrast

from dotenv import load_dotenv

load_dotenv()
import os
from os import path
import discord
import json

intents = discord.Intents.all()
client = discord.Client(intents=intents)
data = None

# CONSTANTS
dark_mode_background = (54/255,57/255,63/255)
white_mode_background = (1,1,1)

def save():
    with open('database.json', 'w') as outfile:
        json.dump(data, outfile)

@client.event
async def on_ready():
    global data
    print('We have logged in as {0.user}'.format(client))
    if path.exists("database.json"):
        with open('database.json', 'r') as f:
            data = json.load(f)
    else:
        data = {}
        save()

    if "event_role_map" not in data.keys():
        data["event_role_map"] = {}
    to_delete = list(data["event_role_map"].keys())
    for guild in client.guilds:
        await guild.fetch_roles()
        evts = await guild.fetch_scheduled_events()
        evt_ids = []
        for e in evts:
            evt_ids.append(e.id)
        for event in await guild.fetch_scheduled_events():
            if str(event.id) not in data["event_role_map"].keys() or not guild.get_role(data["event_role_map"][str(event.id)]):
                await on_scheduled_event_create(event)
            elif event.name != guild.get_role(data["event_role_map"][str(event.id)]).name + " [TPT]":
                await guild.get_role(data["event_role_map"][str(event.id)]).edit(name=event.name + " [TPT]")
            else:
                interested = []
                async for user in event.users():
                    await on_scheduled_event_user_add(event, user)
                    interested.append(user.id)
                associated_role = event.guild.get_role(data["event_role_map"][event.id])
                for m in associated_role.members:
                    if m.id not in interested:
                        await m.remove_roles(associated_role)
        # Mark eid for keeping
        for i in range(len(to_delete) - 1,-1,-1):
            eid = to_delete[i]
            if int(eid) in evt_ids:
                to_delete.remove(eid)
    # Delete unmarked eids
    for eid in to_delete:
        del data["event_role_map"][str(eid)]
    # Delete roles not in event map
    for guild in client.guilds:
        for role in guild.roles:
            if role.name.endswith("[TPT]") and (role.id not in data["event_role_map"].values()):
                await role.delete()
    save()
    print("Finished cleaning up and catching up to events.")

def generate_accessible_colour():
    role_colour = (random(), random(), random())
    contrast_dark = contrast.rgb(role_colour, dark_mode_background)

    # Generate a random colour until it is a good contrast
    attempt = 0
    while contrast_dark < 4.5 and attempt < 25:
        role_colour = (random(), random(), random())
        contrast_dark = contrast.rgb(role_colour, dark_mode_background)
        attempt += 1
    if attempt == 25:
        print("Could not generate a good contrast colour")
    role_colour = (int(role_colour[0] * 255), int(role_colour[1] * 255), int(role_colour[2] * 255))
    role_colour = discord.Color.from_rgb(role_colour[0], role_colour[1], role_colour[2])
    return role_colour

@client.event
async def on_scheduled_event_create(event: discord.ScheduledEvent):
    role = await event.guild.create_role(name=event.name + " [TPT]", mentionable=True, color=generate_accessible_colour())
    data["event_role_map"][str(event.id)] = role.id
    async for user in event.users():
        m = await event.guild.fetch_member(user.id)
        await m.add_roles(role)
    save()

@client.event
async def on_scheduled_event_delete(event: discord.ScheduledEvent):
    print("Event deleted.")
    await event.guild.get_role(data["event_role_map"][str(event.id)]).delete()
    del data["event_role_map"][str(event.id)]

@client.event
async def on_scheduled_event_user_add(event: discord.ScheduledEvent, user: discord.User):
    try:
        m = await event.guild.fetch_member(user.id)
        await m.add_roles(event.guild.get_role(data["event_role_map"][str(event.id)]))
    except:
        print("Could not add user to event.")


@client.event
async def on_scheduled_event_user_remove(event: discord.ScheduledEvent, user: discord.User):
    m = await event.guild.fetch_member(user.id)
    await m.remove_roles(event.guild.get_role(data["event_role_map"][str(event.id)]))

@client.event
async def on_scheduled_event_update(before: discord.ScheduledEvent, after: discord.ScheduledEvent):
    await after.guild.get_role(data["event_role_map"][str(after.id)]).edit(name=after.name + " [TPT]")



@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if client.user in message.mentions:
        await message.channel.send("bonk")

client.run(os.getenv("DISCORD"))

# If modifying these scopes, delete the file token.json.
