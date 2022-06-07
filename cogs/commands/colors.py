import discord
from discord import app_commands
from discord.ext import commands

class colors(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot

    @commands.command(aliases=['colorrole', 'color'])
    async def colors(self, ctx, option):
        """lets you set your color. use config to start. options are; red, orange, yellow, green, blue, purple, cyan, lavender, pink, lime, neon, lemon, rose, and sky."""
        if option == "config":
            await ctx.send("creating color roles...")
            guild = ctx.guild
            await guild.create_role(name="red", colour=discord.Colour(0xFF0000))
            await guild.create_role(name="yellow", colour=discord.Colour(0xFFFF00))
            await guild.create_role(name="orange", colour=discord.Colour(0xFF9900))                
            await guild.create_role(name="green", colour=discord.Colour(0x00FF00))
            await guild.create_role(name="purple", colour=discord.Colour(0x9900FF))
            await guild.create_role(name="blue", colour=discord.Colour(0x0000FF))
            await guild.create_role(name="cyan", colour=discord.Colour(0x29C5EF))
            await guild.create_role(name="lavender", colour=discord.Colour(0xA053EA))
            await guild.create_role(name="pink", colour=discord.Colour(0xE01E64))
            await guild.create_role(name="lime", colour=discord.Colour(0x257208))
            await guild.create_role(name="neon", colour=discord.Colour(0x48DB12))
            await guild.create_role(name="lemon", colour=discord.Colour(0xE5DA0E))
            await guild.create_role(name="rose", colour=discord.Colour(0xD88F8F))
            await guild.create_role(name="sky", colour=discord.Colour(0x358CDB))
            await ctx.send("done!")
            await ctx.send("use ``.colors <color>`` to set your color role!")
            return
        if option == "red":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="red")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")     
            return      
        if option == "yellow":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="yellow")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "orange":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="orange")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "green":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="green")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "purple":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="purple")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "blue":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="blue")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "cyan":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="cyan")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "lavender":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="lavender")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "pink":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="pink")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "lime":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="lime")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "neon":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="neon")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "lemon":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="lemon")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "rose":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="rose")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        if option == "sky":
            user = ctx.message.author
            role = discord.utils.get(ctx.guild.roles, name="sky")
            await user.add_roles(role)
            await ctx.send(f"gave you color {option}!")
            return
        else:
            await ctx.send("incorrect argument. use .help colors for more info")
            return
        
async def setup(bot: commands.Bot):
    await bot.add_cog(colors(bot))