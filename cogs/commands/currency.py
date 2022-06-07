from ext.Config import *
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class money(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot

    @commands.command(aliases=['Money', 'currency'])
    @commands.cooldown(rate=2, per=1800, type=BucketType.user)
    async def money(self, message, option):
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
                Csave()
        if option == 'wallet':
            if user in server_data[message.guild.id]["money"]:
                global balance
                balance = server_data[message.guild.id]["money"][user]
                await message.send(f"you have {balance} coins 🪙")
                return
        if option == 'work':
            if user in server_data[message.guild.id]["money"]:
                server_data[message.guild.id]["money"][user] += 5
                Csave()
                await message.send("you worked! you got 5 N coins 🪙")
                return

    @money.error
    async def do_repeat_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("you're on cooldown! you can only use money commands twice per every 30 minutes!")

    @commands.command()
    async def pay(self, message, userIn: str, value: int):
        """pays someone with N coins!"""
        user = str(message.author.id)
        if userIn is None or value is None:
            await message.send("you must provide both a user and a value!")
            return
        if userIn == str(message.author.id):
            await message.send("you cannot pay yourself!")
            return
        if user in server_data[message.guild.id]["money"]:
            if balance >= value:
                if userIn in server_data[message.guild.id]["money"]:
                    server_data[message.guild.id]["money"][user] -= value
                    server_data[message.guild.id]["money"][userIn] += value
                    Csave()
                    await message.send(f"you payed {userIn} {value} N coins!")
                    return
                else:
                    await message.send(f"{userIn} is not registered!")
                    return
            else:
                await message.send("you can't afford that transaction!")
                return
        else:
            await message.send("you have not registered!")
            return
    
async def setup(bot: commands.Bot):
    await bot.add_cog(money(bot))