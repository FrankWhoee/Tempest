import datetime
import os.path
import random
import time

from dotenv import load_dotenv

load_dotenv()
import os
from os import path
import discord
import json

intents = discord.Intents.all()
client = discord.Client(intents=intents)
data = None

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

    if "event_roles_map" not in data.keys():
        data["event_roles_map"] = {}
    print(data["event_roles_map"])
    for guild in client.guilds:
        await guild.fetch_roles()
        for event in await guild.fetch_scheduled_events():
            if str(event.id) not in data["event_roles_map"].keys() or not guild.get_role(data["event_roles_map"][str(event.id)]):
                await on_scheduled_event_create(event)
            elif event.name != guild.get_role(data["event_roles_map"][str(event.id)]).name + " [TPT]":
                await guild.get_role(data["event_roles_map"][str(event.id)]).edit(name=event.name + " [TPT]")

        # Clean up event_roles_map
        to_delete = []
        for eid in data["event_roles_map"].keys():
            if not guild.get_scheduled_event(int(eid)):
                to_delete.append(eid)

        for eid in to_delete:
            del data["event_roles_map"][str(eid)]

        for role in guild.roles:
            print(role.name.endswith("[TPT]"))
            print(role.id not in data["event_roles_map"].values())
            print(role.name)
            if role.name.endswith("[TPT]") and (role.id not in data["event_roles_map"].values()):
                await role.delete()



@client.event
async def on_scheduled_event_create(event: discord.ScheduledEvent):
    role = await event.guild.create_role(name=event.name + " [TPT]", mentionable=True, color=discord.Color(0).random())
    data["event_roles_map"][str(event.id)] = role.id
    async for user in event.users():
        m = await event.guild.fetch_member(user.id)
        await m.add_roles(role)
    save()

@client.event
async def on_scheduled_event_delete(event: discord.ScheduledEvent):
    print("Event deleted.")
    await event.guild.get_role(data["event_roles_map"][str(event.id)]).delete()
    del data["event_roles_map"][str(event.id)]

@client.event
async def on_scheduled_event_user_add(event: discord.ScheduledEvent, user: discord.User):
    m = await event.guild.fetch_member(user.id)
    await m.add_roles(event.guild.get_role(data["event_roles_map"][str(event.id)]))


@client.event
async def on_scheduled_event_user_remove(event: discord.ScheduledEvent, user: discord.User):
    m = await event.guild.fetch_member(user.id)
    await m.remove_roles(event.guild.get_role(data["event_roles_map"][str(event.id)]))




@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if client.user in message.mentions:
        await message.channel.send("bonk")

client.run(os.getenv("DISCORD"))

# If modifying these scopes, delete the file token.json.
