import discord
from discord import message
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.webhook import AsyncWebhookAdapter
import requests, json, os

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents)
token = 'add token please :)'
server_data = {}

def save_data(guild):
    with open(f"{guild.id}.json", 'w') as fl:
        json.dump(server_data[guild.id], fl, indent=2)

def load_data(guild):
    data = {"mute_role": -1}
    if os.path.exists(f"{guild.id}.json"):
        with open(f'{guild.id}.json', 'r') as fl:
            data = json.load(fl)
    else:
        with open(f'{guild.id}.json', 'w') as fl:
            json.dump(data, fl)

    return data

class MyClient(discord.Client):

    @client.event
    async def on_member_join(member: discord.User):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await guild.system_channel.send(to_send)

    @client.command()
    async def ping(ctx):
        # embed = discord.Embed(title="Ping", description=f"{(int) (client.latency*1000)}ms")
        # await ctx.send(embed=embed)
        await ctx.send(f"Pong! ({(int) (client.latency*1000)}ms)")

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        for guild in client.guilds:
            server_data[guild.id] = load_data(guild)
        await client.change_presence(activity=discord.Streaming(name="coding", url='https://twitch.tv/Morgandri1'))

    global endpoint
    endpoint = "https://api.twitch.tv/kraken/streams/Morgandri1"
    global api
    api = {
        'Client-ID' : 'tqanfnani3tygk9a9esl8conhnaz6wj',
        'Accept' : 'application/vnd.twitchtv.v5+json',
    }

    def checkUser(userID): #returns true if online, false if not
        url = endpoint.format(userID)

        try:
            req = requests.Session().get(url, headers=api)
            jsondata = req.json()
            if 'stream' in jsondata:
                if jsondata['stream'] is not None: #stream is online
                    return True
                else:
                    return False
        except Exception as e:
            print("Error checking user: ", e)
            return False

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        await client.process_commands(message)

    @client.command()
    @has_permissions(administrator=True)
    async def mute(ctx, userIn: str):
        userID = int(userIn.removeprefix("<@!").removesuffix(">").removeprefix("<@"))

        roleID = int(server_data[ctx.guild.id]['mute_role'])
        if roleID == -1:
            await ctx.send("You have not set a mute role!")
        role = ctx.guild.get_role(roleID)
        await ctx.guild.get_member(userID).add_roles(role)
        await ctx.send(f"Muted {userIn}")

    @client.command()
    @has_permissions(administrator=True)
    async def config(ctx, option, value):
        if option is None or value is None or option not in server_data[ctx.guild.id]:
            await ctx.send("invalid")
            return

        if option == 'mute_role':
            value = value.removeprefix("<@&").removesuffix(">")
            if not value.isdigit():
                await ctx.send('integer pls')
                return
            server_data[ctx.guild.id]['mute_role'] = int(value)
            save_data(ctx.guild)
            await ctx.send(f"Set the mute role to id {value}")
            return

        await ctx.send("Failed to do something. idk what. fix")

    @client.command()
    async def hentai(ctx):
        if ctx.channel.is_nsfw():
            url = requests.get(url="https://nekos.life/api/v2/img/hentai").json()['url']
            embed = discord.Embed(title="Here", description="Take some hentai you filthy animal")
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You need to use this command in a nsfw channel!")

    @client.event
    async def on_message(message):
        if "nigga" in message.content:
            await message.delete()

        await client.process_commands(message)


client.run("dont forget me :)")
#made by Morgandri1 and Skizzme
