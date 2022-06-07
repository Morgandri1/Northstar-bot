from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        await ctx.send(
            """
            ```
            Moderation:
                ban - bans a member
                kick - kicks a member
                mute - mutes a member
                unmute - unmutes a member
                purge - clears x messages from a channel
                config - lets you use many configureable systems. use config 
                poll - creates a user poll
            User tools:
                opt - lets a user opt into a role
            Info: 
                links - shows dev links
                debug - shows stats 
                ping - shows client ping
                help - shows this message 
            Fun:
                number - picks a range from 2 numbers 
                meme - sends a meme
                coin - flips a coin
                cat - sends a cat pic
                dog - sends a dog pic
                otter - sends an otter pic
                duck - sends a duck pic
                joke - sends a dad joke
                roast - roasts a member
                snipe - gets last deleted message

            forbidden:
                hentai - you need jesus.
            Math:
                add - adds 2 numbers
                subtract - subtracts 2 numbers
                divide - divides 2 numbers
                multiply - multiplies 2 numbers
            currency:
                money - join, work, wallet
                pay - lets you pay another user with N coin
                
            thanks for using Northstar!
            ```
            """
        )
    
async def setup(bot: commands.Bot):
    await bot.add_cog(help(bot))