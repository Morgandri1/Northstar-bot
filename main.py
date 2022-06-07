import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json, os
import asyncio
import os
from twitchio.ext import eventsub #soon...
from sys import argv
import threading
from flask import Flask
from ext.Config import Csave, Cload, server_data, DefData

intents = discord.Intents(
    messages = True,
    message_content = True, 
    members = True, 
    presences = True,
    guilds = True
)

initial_extensions = [
    'cogs.info.debug',
    'cogs.info.links',
    'cogs.commands.tools',
    'cogs.commands.moderation',
    'cogs.commands.math',
    'cogs.commands.chance',
    'cogs.commands.fun', 
    'cogs.commands.Forbade',
    'cogs.commands.colors',    
    'cogs.commands.currency',
    'cogs.events.events',
    'cogs.info.help',
]

Tfile = open('token.txt', 'r')
Dfile = open('debug.txt', 'r')
token = Tfile.readline()
debugtoken = Dfile.readline()
profiles = {}
snipe_message_content = None
snipe_message_author = None
snipe_message_id = None

#data
version = "4.5.1"
client = commands.Bot(command_prefix=[".", "northstar.", "n.", "N.", ">"], intents=intents)
client.remove_command('help')

#events
@client.event
async def on_ready():
    for cog in initial_extensions:
        await client.load_extension(cog)
        print(f"added {cog}")
    for guild in client.guilds:
        server_data[guild.id] = Cload(guild)
    await client.change_presence(activity=discord.Streaming(name=f"{version}", url='https://twitch.tv/Morgandri1'))
    if guild.system_channel is not None:
        to_send = 'Northstar is back online!'
        await guild.system_channel.send(to_send)
    print(f'We have logged in as {client.user}')
    print(f"""
             _   _            _   _         _             
            | \ | |          | | | |       | |            
            |  \| | ___  _ __| |_| |__  ___| |_ __ _ _ __ 
            | . ` |/ _ \| '__| __| '_ \/ __| __/ _` | '__|
            | |\  | (_) | |  | |_| | | \__ \ || (_| | |   
            \_| \_/\___/|_|   \__|_| |_|___/\__\__,_|_|     {version} 
            
                    Logged in and ready
                made with ❤️  by Morgandri1
            """)

#commands
@client.command(aliases=['role', 'roles'])
async def opt(ctx, value):
    """allows users to opt into roles"""
    user = ctx.message.author
    data = server_data[ctx.guild.id]["publicroles"]
    if data != -1:
        role = discord.utils.get(ctx.guild.roles, id=data)
        await user.add_roles(role)
        await ctx.send(f"gave you role {value}!")     
        return     
    else:
        await ctx.send("that role is not public!")

#control
async def StartBot():
    async with client:
        await client.start(str(debugtoken))

async def main():
  async with client:
    await client.start(str(token))

async def debugmain():
  async with client:
    await client.start(str(debugtoken))

app = Flask("")

@app.route("/")
def home():
    servers = str(len(client.guilds))
    return f"Registered to {servers} guilds\nping is {(int)(client.latency * 1000)}ms"

def run():
    app.run(host="0.0.0.0",port=7000)

if argv[1] == 'debug': #debug mode to not annoy people and avoid overhyping features that dont get added
    P = threading.Thread(target=run)
    P.start()
    print("server started")
    print("debug mode")
    asyncio.run(debugmain())
elif argv[1] == "app":
    P = threading.Thread(target=run)
    P.start()
    print("server started")
    print("release mode")
    asyncio.run(main())
