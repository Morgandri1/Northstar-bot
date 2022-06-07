import discord
from discord import app_commands
from discord.ext import commands
from ext.Config import *

class moderation(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot

    @commands.command(aliases=['yeet'])
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """kicks a member"""
        if reason == None:
            reason = "no reason provided"
            await ctx.guild.kick(member)
            await ctx.send(f'User {member.mention} has been kicked for ``{reason}``')

    @commands.command(aliases=['banhammer', 'bonk', 'kill'])
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """bans a member"""
        if reason == None:
            reason = "no reason provided"
            await ctx.guild.ban(member)
            await ctx.send(f'User {member.mention} has been banned for ``{reason}``')

        
    @commands.command(aliases=['silence'])
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, userIn: str):
        """allows mods to mute a user"""
        userID = int(userIn.removeprefix("<@!").removesuffix(">").removeprefix("<@"))
        roleID = int(server_data[ctx.guild.id]['mute_role'])
        if roleID == -1:
            await ctx.send("You have not set a mute role!")
        role = ctx.guild.get_role(roleID)
        await ctx.guild.get_member(userID).add_roles(role)
        await ctx.send(f"Muted {userIn}") 

    @commands.command(aliases=['unsilence'])
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, userIn: str):
        """allows mods to unmute a user"""
        userID = int(userIn.removeprefix("<@!").removesuffix(">").removeprefix("<@"))

        roleID = int(server_data[ctx.guild.id]['mute_role'])
        if roleID == -1:
            await ctx.send("You have not set a mute role!")
        role = ctx.guild.get_role(roleID)
        await ctx.guild.get_member(userID).remove_roles(role)
        await ctx.send(f"Unmuted {userIn}")

        
async def setup(bot: commands.Bot):
    await bot.add_cog(moderation(bot))