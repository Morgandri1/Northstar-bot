from http.client import FAILED_DEPENDENCY
import discord
from discord import app_commands
from discord.ext import commands
from ext.Config import *

class tools(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot

    @commands.command(aliases=['polls'])
    @commands.has_permissions(administrator=True)
    async def poll(self, message, option):
        """allows admins to easily create polls"""
        m = await message.send(option)
        await m.add_reaction("⬆️")
        await m.add_reaction("⬇️")

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        await ctx.send("""no option passed! options are:
            ```
            mute_role - the designated mute role
            pussies - people not to roast
            streamer - set streamer to alert the server about [COMING SOON]
            join_role - the role to give to new members
            join_message - the message to send upon member join
            leave_message - what message to send upon member leave
            opt - set a user opt-in role
            filter - naughty words
            ```
            """)

    @config.command()
    @commands.has_permissions(administrator=True)
    async def mute_role(self, ctx, value):
        value = value.removeprefix("<@&").removeprefix("<@").removesuffix(">")
        if not value.isdigit():
            await ctx.send('integer not passed')
            return
        server_data[ctx.guild.id]['mute_role'] = int(value)
        Csave()
        await ctx.send(f"Set the mute role to id {value}")
        return
        
    @config.command()
    @commands.has_permissions(administrator=True)
    async def pussies(self, ctx, value):
        value = value.removeprefix("<@").removesuffix(">")
        if not value.isdigit():
            await ctx.send('integer not passed')
            return
        server_data[ctx.guild.id]['pussies'].append(value)
        Csave()
        await ctx.send(f"Added <@{value}> to the list of pussies")
        return
    
    @config.command()
    @commands.has_permissions(administrator=True)
    async def filter(self, ctx, value):
        filters = server_data[ctx.guild.id]['filter']
        if filter in filters:
            await ctx.send("already added to the list of filters")
            return
        filters.append(value)
        Csave()
        await ctx.send("appended the filter list")
        return  
    
    @config.command()
    @commands.has_permissions(administrator=True)
    async def join_message(self, ctx, value):
        msg = value
        data = server_data[ctx.guild.id]['join_message']
        if data != -1:
            await ctx.send(f"you already have a message set! it is currently ``{data}``")
        else:
            server_data[ctx.guild.id]["join_message"] = str(msg)
            Csave()
            await ctx.send("set welcome message.")
        return

    @config.command()
    @commands.has_permissions(administrator=True)
    async def join_role(self, ctx, value):
        value = value.removeprefix("<@&").removeprefix("<@").removesuffix(">")
        roleID = int(value)
        data = server_data[ctx.guild.id]['join_role']
        if data != -1:
            await ctx.send("you already have a join role set!")
        else:
            server_data[ctx.guild.id]['join_role'] = int(roleID)
            Csave()
            await ctx.send("set your join role.")
        return

    @config.command()
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx, value):
        value = value.removeprefix("<#").removesuffix(">")
        channel = value
        data = server_data[ctx.guild.id]["Welcome"]
        if data != -1:
            await ctx.send("your already have a Welcome channel set! use ``.config clear welcome`` to reset it.")
        else:
            server_data[ctx.guild.id]['Welcome'] = int(channel)
            Csave()
            await ctx.send("set your welcome channel.")
        return

    @config.command()
    @commands.has_permissions(administrator=True)
    async def announcement(self, ctx, value):
        value = value.removeprefix("<#").removesuffix(">")
        channel = value
        data = server_data[ctx.guild.id]["announcement"]
        if data != -1:
            await ctx.send("you have already set an announcement channel. use ``.config clear announcment`` to reset it.")
        else:
            server_data[ctx.guild.id]['announcement'] = int(channel)
            Csave()
            await ctx.send("added an announcement channel.")
        return
        
    @config.command()
    @commands.has_permissions(administrator=True)
    async def leave_message(self, ctx, value):
        msg = value
        data = server_data[ctx.guild.id]['leave_message']
        if data != -1:
            await ctx.send(f"you already have a message set! it is currently ``{data}``")
        else:
            server_data[ctx.guild.id]["leave_message"] = str(msg)
            Csave()
            await ctx.send("set leave message.")
        return

    @config.command()
    @commands.has_permissions(administrator=True)
    async def opt(self, ctx, value):
        value = value.removeprefix("<@&").removeprefix("<@").removesuffix(">")
        roleID = int(value)
        server_data[ctx.guild.id]['publicroles'] = int(roleID)
        Csave()
        await ctx.send("added an opt role.")
        return

    @config.command()
    @commands.has_permissions(administrator=True)
    async def streamer(self, ctx, value):
        streamer = value
        data = server_data[ctx.guild.id]['streamer']
        if data != -1:
            await ctx.send("you already have a streamer set! use ``.config clear streamer`` to reset it")
        else:
            server_data[ctx.guild.id]["streamer"] = str(streamer)
            Csave()
            await ctx.send("appended streamer. you'll get notified when they go live.")
        return

    @config.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, value):
        if value is None or value == "all":
            server_data[ctx.guild.id] == DefData
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        if value == "mute_role":
            server_data[ctx.guild.id]["mute_role"] = -1
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        if value == "pussies":
            server_data[ctx.guild.id]["pussies"] = []
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        if value == "filter":
            server_data[ctx.guild.id]["filter"] = []
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        if value == "money": 
            server_data[ctx.guild.id]["money"] = {}
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        if value == "announcement":
            server_data[ctx.guild.id]["announcement"] = -1
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        if value == "welcome":
            server_data[ctx.guild.id]["Welcome"] = -1
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        if value == "join_message":
            server_data[ctx.guild.id]["join_message"] = -1
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        if value == "join_role":
            server_data[ctx.guild.id]["join_role"] = -1
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        if value == "opt":
            server_data[ctx.guild.id]["publicroles"] = -1
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        if value == "leave_message":
            server_data[ctx.guild.id]["leave_message"] = -1
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        if value == "streamer":
            server_data[ctx.guild.id]["streamer"] = -1
            Csave()
            await ctx.send(f"cleared data from {value}")
            return
        else: 
            await ctx.send(f"error! {value} is an incorrect argument.")
            return   


async def setup(bot: commands.Bot):
    await bot.add_cog(tools(bot))