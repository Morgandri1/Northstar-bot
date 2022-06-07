import discord
from discord import app_commands
from discord.ext import commands
import random
import aiohttp
from ext.Config import *
import asyncio

snipe_message_content = None
snipe_message_author = None
snipe_message_id = None

class events(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, members):
        people = len(guild.member_count)
        guild = members.guild
        global channel
        channel = self.bot.get_channel(server_data[guild.id]['Welcome'])
        if server_data[guild.id]['join_message'] == -1:
            try:
                to_send = f'Welcome {members.mention} to {guild.name}! member count: {people}'
                await channel.send(to_send)
            except AttributeError:
                print("no welcome channel found")
        if server_data[guild.id]['join_role'] != -1:
                roleID = server_data[guild.id]["join_role"]
                role = discord.utils.get(members.guild.roles, id=roleID)
                await members.add_roles(role)
        else:
            to_send = server_data[guild.id]['join_message']
            await channel.send(to_send)
        return

    @commands.Cog.listener()
    async def on_member_remove(self, members):
        people = len(discord.guild.member_count)
        guild = members.guild
        global channel
        channel = self.bot.get_channel(server_data[guild.id]['Welcome'])
        if server_data[guild.id]['leave_message'] == -1:
            try:
                to_send = f'dang. {members.mention} has left. this is so sad. alexa, play despacito. member count: {people}'
                await channel.send(to_send)
            except AttributeError:
                return
        else:
            to_send = server_data[guild.id]['leave_message']
            await channel.send(to_send)
        return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content in server_data[message.guild.id]['filter']:
            await message.delete()
        if message.channel.id == server_data[message.guild.id]['announcement']:
            await message.add_reaction("⬆️")
            await message.add_reaction("⬇️")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print("delete")
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

    @commands.command(aliases=['deleted'])
    async def snipe(self, message):
        """gets a record of the last deleted message"""
        if snipe_message_content == None:
            await message.channel.send("There's nothing to snipe!")
        else:
            embed = discord.Embed(title="caught in 4k", description=f"{snipe_message_content}")
            embed.set_footer(text=f"Asked by {message.author.name}#{message.author.discriminator}",
                            icon_url=message.author.avatar_url)
            embed.set_author(name=f"{message.author.name}")
            await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error): 
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("command not found! use ``.help`` for a commands list.")

async def setup(bot: commands.Bot):
    await bot.add_cog(events(bot))