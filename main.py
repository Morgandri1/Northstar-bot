from multiprocessing.sharedctypes import Value
from unittest import result
import discord
from discord import message
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.webhook import AsyncWebhookAdapter
from numpy import true_divide
import requests, json, os
import asyncio
import random
import aiohttp
from async_timeout import timeout
from functools import partial
import os
from bs4 import BeautifulSoup
from discord.ext.commands.cooldowns import BucketType

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents)
Tfile = open('token.txt', 'r')
token = Tfile.readline()
server_data = {}
snipe_message_content = None
snipe_message_author = None
snipe_message_id = None

#client information
def save_data():
    with open(f"configs.json", 'w') as fl:
        json.dump(server_data, fl, indent=2)

def load_data(guild):
    global DefData
    DefData = {"mute_role": -1, "pussies": [], "filter": [], "money": {}}  # use <@userid>
    if os.path.exists(f"configs.json"):
        with open(f'configs.json', 'r') as fl:
            loaded = json.load(fl)
            if f"{guild.id}" in loaded:
                DefData = loaded[f"{guild.id}"]
    else:
        with open(f'configs.json', 'w') as fl:
            json.dump(DefData, fl)

    return DefData

#server information
class MyClient(discord.Client):
    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        print("""
                 _   _            _   _         _             
                | \ | |          | | | |       | |            
                |  \| | ___  _ __| |_| |__  ___| |_ __ _ _ __ 
                | . ` |/ _ \| '__| __| '_ \/ __| __/ _` | '__|
                | |\  | (_) | |  | |_| | | \__ \ || (_| | |   
                \_| \_/\___/|_|   \__|_| |_|___/\__\__,_|_|   
                
                        Logged in and ready
                     made with ❤️  by Morgandri1
                    """)
        for guild in client.guilds:
            server_data[guild.id] = load_data(guild)
        await client.change_presence(activity=discord.Streaming(name="v2.1", url='https://twitch.tv/Morgandri1'))

    @client.event
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await guild.system_channel.send(to_send)

    @client.event
    async def on_message(message):
        if message.content in server_data[message.guild.id]['filter']:
            await message.delete()
        await client.process_commands(message)

    @client.command()
    @commands.cooldown(rate=2, per=1800, type=BucketType.user)
    async def money(message, option):
        """.money join to start!"""
        user = str(message.author.id)
        if option is None:
            await message.send("invalid")
            return
        if option == 'join':
            data = server_data[message.guild.id]["money"]
            if user in data:
                await message.send("you are already registered!")                
            else:
                server_data[message.guild.id]["money"][user] = 0
                await message.send("added user to the economy! 🪙")
                save_data()
        if option == 'wallet':
            if user in server_data[message.guild.id]["money"]:
                global balance
                balance = server_data[message.guild.id]["money"][user]
                await message.send(balance)
        if option == 'work':
            if user in server_data[message.guild.id]["money"]:
                server_data[message.guild.id]["money"][user] += 5
                save_data()
                await message.send("you worked! you got 5 N coins.")

    #currency error handler
    @money.error
    async def do_repeat_handler(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("you're on cooldown! you can only use money commands once per every 30 minutes!")

    @client.command()
    async def pay(message, userIn: str, value: int):
        """pays someone with N coins!"""
        user = str(message.author.id)
        if user in server_data[message.guild.id]["money"]:
            if balance >= value:
                if userIn in server_data[message.guild.id]["money"]:
                    server_data[message.guild.id]["money"][user] -= value
                    save_data()
                    await message.send(f"you payed {userIn} {value} N coins!")
                else:
                    await message.send(f"{userIn} is not registered!")
            
    @client.command()
    async def stackstat(ctx):
        """gets the status of stackoverflow"""
        url = 'https://www.stackoverflow.com/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        for title in soup.find_all('title'):
            if title.get_text() == "Stack Overflow - Where Developers Learn, Share, & Build Careers":
                await ctx.send('stackoverflow is up!')
            else:
                await ctx.send('stackoverflow is down!')

    @client.command()
    async def ping(ctx):
        """shows the response time"""
        # embed = discord.Embed(title="Ping", description=f"{(int) (client.latency*1000)}ms")
        # await ctx.send(embed=embed)
        await ctx.send(f"Pong! ({(int)(client.latency * 1000)}ms)")

    @client.command()
    async def links(ctx):
        """displays a list of Morgandril's links"""
        await ctx.send("github: https://github.com/Morgandri1 \ntwitch: https://twitch.tv/Morgandri1")

    global endpoint
    endpoint = "https://api.twitch.tv/kraken/streams/Morgandri1"
    global api
    api = {
        'Client-ID': 'tqanfnani3tygk9a9esl8conhnaz6wj',
        'Accept': 'application/vnd.twitchtv.v5+json',
    }

    def checkUser(userID):  # returns true if online, false if not
        url = endpoint.format(userID)

        try:
            req = requests.Session().get(url, headers=api)
            jsondata = req.json()
            if 'stream' in jsondata:
                if jsondata['stream'] is not None:  # stream is online
                    return True
                else:
                    return False
        except Exception as e:
            print("Error checking user: ", e)
            return False

    @client.command()
    @has_permissions(administrator=True)
    async def mute(ctx, userIn: str):
        """allows mods to mute a user"""
        userID = int(userIn.removeprefix("<@!").removesuffix(">").removeprefix("<@"))
        roleID = int(server_data[ctx.guild.id]['mute_role'])
        if roleID == -1:
            await ctx.send("You have not set a mute role!")
        role = ctx.guild.get_role(roleID)
        await ctx.guild.get_member(userID).add_roles(role)
        await ctx.send(f"Muted {userIn}") 

    @client.command()
    @has_permissions(administrator=True)
    async def unmute(ctx, userIn: str):
        """allows mods to unmute a user"""
        userID = int(userIn.removeprefix("<@!").removesuffix(">").removeprefix("<@"))

        roleID = int(server_data[ctx.guild.id]['mute_role'])
        if roleID == -1:
            await ctx.send("You have not set a mute role!")
        role = ctx.guild.get_role(roleID)
        await ctx.guild.get_member(userID).remove_roles(role)
        await ctx.send(f"Unmuted {userIn}")

    @client.event
    async def on_message_delete(message):

        global snipe_message_content
        global snipe_message_author
        global snipe_message_id

        snipe_message_content = message.content
        snipe_message_author = message.author.id
        snipe_message_id = message.id
        await asyncio.sleep(60)

        if message.id == snipe_message_id:
            snipe_message_author = None
            snipe_message_content = None
            snipe_message_id = None

    @client.command()
    async def snipe(message):
        """gets a record of the last deleted message"""
        if snipe_message_content == None:
            await message.channel.send("Theres nothing to snipe.")
        else:
            embed = discord.Embed(title="caught in 4k", description=f"{snipe_message_content}")
            embed.set_footer(text=f"Asked by {message.author.name}#{message.author.discriminator}",
                             icon_url=message.author.avatar_url)
            embed.set_author(name=f"{message.author.name}")
            await message.channel.send(embed=embed)
            return

    @client.command()
    @has_permissions(administrator=True)
    async def config(ctx, option, value):
        """options: filter, muterole, people to not roast, clear"""
        if option is None or value is None:
            await ctx.send("invalid operation")
            return

        if option == "clear":
            if value is None or value == "all":
                server_data[ctx.guild.id] == DefData
            if value == "mute_role":
                server_data[ctx.guild.id]["mute_role"] == -1
            if value == "pussies":
                server_data[ctx.guild.id]["pussies"] == []
            if value == "filter":
                server_data[ctx.guild.id]["filter"] == []
            if value == "money": 
                server_data[ctx.guild.id]["money"] == {}
            save_data()
            await ctx.send(f"cleared data from {value}")
            return

        if option == 'mute_role':
            value = value.removeprefix("<@&").removeprefix("<@").removesuffix(">")
            if not value.isdigit():
                await ctx.send('integer not passed')
                return
            server_data[ctx.guild.id]['mute_role'] = int(value)
            save_data()
            await ctx.send(f"Set the mute role to id {value}")
            return

        if option == "pussies":
            value = value.removeprefix("<@&").removesuffix(">")
            if not value.isdigit():
                await ctx.send('integer not passed')
                return
            server_data[ctx.guild.id]['pussies'].append(value)
            save_data()
            await ctx.send(f"Added <@{value}> to the list of pussies")
            return
        
        if option == "filter":
            filters = server_data[ctx.guild.id]['filter']
            if filter in filters:
                await ctx.send("already added to the list of filters")
                return
            filters.append(value)
            save_data()
            await ctx.send("appended the filter list")
            return           

        await ctx.send("Failed to do something. idk what. fix")

    @client.command()
    async def hentai(ctx):
        """y'all need jesus"""
        if ctx.channel.is_nsfw():
            url = requests.get(url="https://nekos.life/api/v2/img/pussy").json()['url']
            embed = discord.Embed(title="Here", description="Take some hentai you filthy animal")
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You need to use this command in a nsfw channel!")

    @client.command()
    @commands.has_permissions(administrator=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        """kicks a member"""
        if reason == None:
            reason = "no reason provided"
            await ctx.guild.kick(member)
            await ctx.send(f'User {member.mention} has been kicked for ``{reason}``')

    @client.command()
    @commands.has_permissions(administrator=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        """bans a member"""
        if reason == None:
            reason = "no reason provided"
            await ctx.guild.ban(member)
            await ctx.send(f'User {member.mention} has been banned for ``{reason}``')

    @client.command()
    async def roast(ctx, member: discord.Member):
        """roast's the mentioned member"""
        # is_pussy = member.id in server_data[ctx.guild.id]['pussies']
        # for id in server_data[ctx.guild.id]:
        #     if id == member.id
        if f"{member.id}" in server_data[ctx.guild.id]['pussies']:
            await ctx.send(f"{member.mention}'s pretty cool!")
        else:
            roasts = [
                f"{member.mention}'s GPA may be high but the number of bitches on their dick is low",
                f"I would roast {member.mention}, but my mom said I shouldnt burn trash",
                f"I wish I could meet {member.mention} again and walk away this time",
                f"whoever told {member.mention} to be themselves was lying",
                f"sorry i can't think of an insult dumb enough for {member.mention} to understand",
                f"i would call {member.mention} an idiot but that would be an insult to stupid people",
                f"No breath mint can obscure the sheer stench of the bullshit that just came out of {member.mention}'s mouth just now."
            ]
            index = random.randrange(0, len(roasts))
            await ctx.send(roasts[index])
            print(member.mention)

    @client.command()
    async def joke(ctx):
        """sends a random dad joke"""
        jokes = [
            'Why did the football coach go to the bank? To get his quarter back.',
            'Why cant a leopard hide? Hes always spotted.',
            'Air used to be free at the gas station, now it costs 2.50. You want to know why? Inflation.',
            'I tried to get a smart car the other day but they sold out too fast. Why? I guess Im just a bit slow.',
            'I told my wife that a husband is like a fine wine: we just get better with age. The next day she locked me in the cellar.',
            "Why does a husband lead a dog's life? He comes in with muddy feet, gets comfortable by the fire, and waits to be fed.",
            "Did you hear about the claustrophobic astronaut? He just wanted a bit more space.",
            "What does the stork do once he's delivered the baby? He lies on the couch and drinks a beer!",
            "How many telemarketers does it take to change a light bulb? Only one, but he has to do it during dinner.",
            "Why did the orange lose the race? It ran out of juice.",
            "How you fix a broken pumpkin? With a pumpkin patch.",
            "Why are fish so smart? They live in schools!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
            "Why did the man fall down the well? Because he couldn’t see that well!",
            "Why do peppers make such good archers? Because they habanero.",
            "What did the sink tell the toilet? You look flushed!",
            "why was the ant confused? because all of his undles were aunts!"
            "i asked my german friend what the square root of 81 was. he said no."
        ]
        index = random.randrange(0, len(jokes))
        await ctx.send(jokes[index])

    @client.command()
    async def duck(ctx):
        """sends a picture of a duck"""
        links = [
            "https://c.tenor.com/AQecc2g8uuAAAAAC/duck-dance.gif",
            "https://c.tenor.com/xxeMW4g1NTAAAAAC/duck-dancing-duck.gif",
            "https://upload.wikimedia.org/wikipedia/commons/a/a1/Mallard2.jpg",
            "https://www.thespruce.com/thmb/t13CIs9CH0HfuggdQ-DU9zk_QHo=/3780x2126/smart/filters:no_upscale()/do-ducks-have-teeth-4153828-hero-9614a7e9f4a049b48e8a35a9296c562c.jpg",
            "https://www.cnet.com/a/img/C4R_F8PD965L7Eakym2BWbk3O6s=/1200x630/2019/01/09/e30a81d2-f4e7-4439-98bf-61e288e16007/gettyimages-1045983738-1.jpg",
            "https://cdn.vox-cdn.com/thumbor/Wd-2zsFlWxXz1HgmGEEwXx5iYBI=/0x0:1000x605/1200x800/filters:focal(420x223:580x383)/cdn.vox-cdn.com/uploads/chorus_image/image/48780381/duck.0.png",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTn-GmO6ktjq8lB8zWnn8bEZzPK00gD7skuVg&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7qbhatJNmhUe9ZqRhEo1IgB5I_bnkrjCX7Q&usqp=CAU",
            "https://i.guim.co.uk/img/media/e0a3aa9884c7ff7e4a2a4351b6a5340e72368f0a/0_184_720_432/master/720.jpg?width=1200&quality=85&auto=format&fit=max&s=b47eed5571c5072dc81bef6cd70adf91",
        ]
        index = random.randrange(0, len(links))
        embed = discord.Embed(title="Duck", description="a picture of a duck")
        embed.set_image(url=links[index])
        await ctx.send(embed=embed)

    @client.command()
    async def cat(ctx):
        """sends a cat picture"""
        links = [
            "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/cute-cat-photos-1593441022.jpg?crop=0.669xw:1.00xh;0.166xw,0&resize=640:*",
            "https://images.unsplash.com/photo-1529778873920-4da4926a72c2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8Y3V0ZSUyMGNhdHxlbnwwfHwwfHw%3D&w=1000&q=80",
            "https://filmdaily.co/wp-content/uploads/2020/04/cute-cat-videos-lede-1300x882.jpg",
            "https://st1.latestly.com/wp-content/uploads/2021/08/31-6-784x441.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxXwz_aEcFGuXxbZx_vtCm3oIjpmO4Wmljug&usqp=CAU",
            "https://c.tenor.com/yheo1GGu3FwAAAAM/rick-roll-rick-ashley.gif",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgQZsLeDJcyOkhxr6ePwiBTla8YgljqFrIIw&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQuQl3_fbyN6nylNXIQ3N0L8Un_qTqVQ2VFRw&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNoFoDT2i40xTf9bAQbgL4YLQewb-4bSt6CA&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpdbrLlhVnaa0wldvuZqbF9dTSLz67HBAR4A&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbi0nRsf_MXf9LShlNY6vRMEgisddL-tBcoA&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7AdwCXShyDM6ZvcKFCTy898b_KKF7BCxdzQ&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSI5zoJRBJCAndOV13vCPQb1F_E4Zsg_zSu7w&usqp=CAU",
        ]
        index = random.randrange(0, len(links))
        embed = discord.Embed(title="Cat", description="a picture of a cat")
        embed.set_image(url=links[index])
        await ctx.send(embed=embed)

    @client.command()
    async def dog(ctx):
        """sends a dog picture"""
        links = [
            "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=1.00xw:0.669xh;0,0.190xh&resize=1200:*",
            "http://cdn.akc.org/content/article-body-image/golden_puppy_dog_pictures.jpg",
            "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8ZG9nc3xlbnwwfHwwfHw%3D&w=1000&q=80",
            "https://post.medicalnewstoday.com/wp-content/uploads/sites/3/2020/02/322868_1100-800x825.jpg",
            "https://ggsc.s3.amazonaws.com/images/uploads/The_Science-Backed_Benefits_of_Being_a_Dog_Owner.jpg",
            "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/smartest-dog-breeds-1553287693.jpg?crop=0.673xw:1.00xh;0.167xw,0&resize=640:*",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT36OGUq8X23zUYSRF3TEcQCcZbxdZvIphwcQ&usqp=CAU",
            "https://www.hemeltoday.co.uk/webimg/b25lY21zOjE0MWMyMWM1LTE5MTItNDZlYy1hMjljLTAxNGUwMGM4N2Y1YTo4ZjVmMjQ2Mi02M2Q2LTQ2YzEtOWZmMS1jY2ZjOWI5NmE3YmM=.jpg?width=640&enable=upscale",
            "https://cdn.britannica.com/q:60/49/161649-050-3F458ECF/Bernese-mountain-dog-grass.jpg",
            "https://www.guidedogs.org/wp-content/uploads/2021/11/01.11.2021_SGD1014-Edit-scaled.jpg",
            "https://images.unsplash.com/photo-1611003228941-98852ba62227?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8YmFieSUyMGRvZ3xlbnwwfHwwfHw%3D&w=1000&q=80",
            "https://hips.hearstapps.com/ghk.h-cdn.co/assets/16/08/gettyimages-464163411.jpg",
            "https://media.nature.com/lw800/magazine-assets/d41586-020-03053-2/d41586-020-03053-2_18533904.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxYy4mS5E0-eG5aKeoTPTtkwal628dGFsrgA&usqp=CAU",
        ]
        index = random.randrange(0, len(links))
        embed = discord.Embed(title="Dog", description="a picture of a dog")
        embed.set_image(url=links[index])
        await ctx.send(embed=embed)
    
    @client.command()
    async def otter(ctx):
        """sends an otter picture"""
        links = [
            "https://images.immediate.co.uk/production/volatile/sites/23/2016/08/GettyImages-557059821-836aa91.jpg?quality=90&resize=620%2C413",
            "https://static01.nyt.com/images/2021/07/08/science/08TB-OTTERS1/08TB-OTTERS1-mobileMasterAt3x.jpg",
            "https://gifts.worldwildlife.org/gift-center/Images/large-species-photo/large-Sea-Otter-photo.jpg",
            "https://ichef.bbci.co.uk/news/976/cpsprodpb/3B4B/production/_109897151_otternew.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTn1bX32I9XM7P3cp4Qt_NvcfhnzhXyzcoOPA&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7LEmIrQhurLH6iNi8AGPIVSamJuvEc-OUfA&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwdlMkT4O914pqlU-DVdI5PR6kPM0m8f1v_A&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHlk5B2-nI25ybGchetck86CwJB2KT6pLjew&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxGQFqS52ZucYEWwUsLioNkOo5p1ZRO7vydQ&usqp=CAU",
            "https://www.otterspecialistgroup.org/osg-newsite/wp-content/uploads/2017/04/ThinkstockPhotos-827261360.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSNULFqAJo3y1WxcM2BIBOBPyjQ2PjQfGdEQ&usqp=CAU",
            "https://globalnews.ca/wp-content/uploads/2018/12/Abby-otter-thicc.jpg?quality=85&strip=all&w=720&h=379&crop=1",
            "https://www.calparks.org/sites/default/files/2019-09/iStock-1059316898_0.jpg",
            "https://i.guim.co.uk/img/media/76c3d4490e882c62c7d2eae593426da1da8d0d0f/0_418_4800_2879/master/4800.jpg?width=1200&quality=85&auto=format&fit=max&s=499a5a77abf39f360778cc08700178aa"
        ]
        index = random.randrange(0, len(links))
        embed = discord.Embed(title="Otter", description="a picture of an Otter")
        embed.set_image(url=links[index])
        await ctx.send(embed=embed)

    @client.command(pass_context=True)
    async def meme(ctx):
        """sends a meme"""
        embed = discord.Embed(title="here's a meme", description="from r/memes")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @client.command()
    async def add(ctx, left: int, right: int):
        """adds two numbers"""
        await ctx.send(left + right)
        
    @client.command()
    async def multiply(ctx, left: int, right: int):
        """multiplies two numbers"""
        await ctx.send(left * right)

    @client.command()
    async def divide(ctx, left: int, right: int):
        """divides two numbers"""
        await ctx.send(left / right)

    @client.command()
    async def coin(ctx):
        """flips a coin"""
        flip = [
            "heads",
            "tails"
        ]
        index = random.randrange(0, len(flip))
        await ctx.send(flip[index])

    @client.command()
    async def roll(ctx, dice: str):
        """ex: .roll 1d6"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

#print(str(token))     #debug only
client.run(str(token))