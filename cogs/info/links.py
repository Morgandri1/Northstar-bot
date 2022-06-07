import discord
from discord import app_commands
from discord.ext import commands

class links(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot

    @commands.command(aliases=['link'])
    async def links(self, ctx):
        """displays a list of Morgandril's links"""
        await ctx.send("github: https://github.com/Morgandri1 \ntwitch: https://twitch.tv/Morgandri1\ntwitter: https://twitter.com/morgandri1dev/")

async def setup(bot):
    await bot.add_cog(links(bot))