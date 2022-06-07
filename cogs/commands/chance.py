import discord
from discord import app_commands
from discord.ext import commands
import random

class chance(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot

    @commands.command(aliases=['flip'])
    async def coin(self, ctx):
        """flips a coin"""
        flip = [
            "heads",
            "tails"
        ]
        index = random.randrange(0, len(flip))
        await ctx.send(flip[index])

    @commands.command(aliases=['random'])
    async def number(self, ctx, value1=int(), value2=int()):
        """picks a number. ex: .number 1 10"""
        if value1 is None or value2 is None:
            await ctx.send("must have 2 values")
        if value1 == value2:
            await ctx.send("must have 2 different numbers")
        rand = int(random.randint(value1-1, value2-1))
        await ctx.send(f"picked {rand} from {value1}-{value2}")
    
async def setup(bot: commands.Bot):
    await bot.add_cog(chance(bot))