from click import command
from discord.ext import commands

class debug(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot

    @commands.command(aliases=['Ping', 'pong'])
    async def ping(self, ctx):
        """shows the response time"""
        await ctx.send(f"Pong! ({(int)(self.bot.latency * 1000)}ms)")

    @commands.command(aliases=['info'])
    async def debug(self, message):
        """shows bot info"""
        servers = str(len(self.bot.guilds))
        await message.channel.send(f"i'm registered to {servers} guilds!")
        await message.channel.send(f"my prefixes are ``., >, N., and northstar.``")
        await message.channel.send(f"made with ❤️ by Morgandri1")
        await message.channel.send(f"ping is {(int)(self.bot.latency * 1000)}ms")
        return
    
async def setup(bot: commands.Bot):
    await bot.add_cog(debug(bot))