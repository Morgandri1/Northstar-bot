from discord.ext import commands

class math(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot

    @commands.command(aliases=['addition'])
    async def add(ctx, left: int, right: int):
        """adds two numbers"""
        await ctx.send(left + right)

    @commands.command(aliases=['difference'])
    async def subtract(ctx, left: int, right: int):
        """subtracts two numbers"""
        await ctx.send(left - right)

    @commands.command()
    async def multiply(ctx, left: int, right: int):
        """multiplies two numbers"""
        await ctx.send(left * right)

    @commands.command()
    async def divide(ctx, left: int, right: int):
        """divides two numbers"""
        await ctx.send(left / right)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(math(bot))