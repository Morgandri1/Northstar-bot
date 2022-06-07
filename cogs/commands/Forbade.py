import discord
from discord.ext import commands
import requests

class forbidden(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot

    @commands.command(aliases=['porn', 'horni'])
    async def hentai(self, ctx):
        """y'all need jesus"""
        if ctx.channel.is_nsfw():
            url = requests.get(url="https://nekos.life/api/v2/img/pussy").json()['url']
            embed = discord.Embed(title="Here", description="Take some hentai you filthy animal")
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You need to use this command in a nsfw channel!")
    
async def setup(bot: commands.Bot):
    await bot.add_cog(forbidden(bot))