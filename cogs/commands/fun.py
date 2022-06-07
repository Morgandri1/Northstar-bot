import discord
from discord import app_commands
from discord.ext import commands
import random
import aiohttp
from ext.Config import *

class fun(commands.Cog):
    def __init__(self, bot):
        super().__init__()  # this is now required in this context.
        self.bot = bot

    @commands.command()
    async def otter(self, ctx):
        """sends an otter picture"""
        links = [
            "https://images.immediate.co.uk/production/volatile/sites/23/2016/08/GettyImages-557059821-836aa91.jpg?quality=90&resize=620%2C413",
            "https://static01.nyt.com/images/2021/07/08/science/08TB-OTTERS1/08TB-OTTERS1-mobileMasterAt3x.jpg",
            "https://gifts.worldwildlife.org/gift-center/Images/large-species-photo/large-Sea-Otter-photo.jpg",
            "https://ichef.bbci.co.uk/news/976/cpsprodpb/3B4B/production/_109897151_otternew.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTn1bX32I9XM7P3cp4Qt_NvcfhnzhXyzcoOPA&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7LEmIrQhurLH6iNi8AGPIVSamJuvEc-OUfA&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwdlMkT4O914pqlU-DVdI5PR6kPM0m8f1v_A&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHlk5B2-nI25ybGchetck86CwJB2KT6pLjew&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxGQFqS52ZucYEWwUsLioNkOo5p1ZRO7vydQ&usqp=CAU",
            "https://www.otterspecialistgroup.org/osg-newsite/wp-content/uploads/2017/04/ThinkstockPhotos-827261360.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSNULFqAJo3y1WxcM2BIBOBPyjQ2PjQfGdEQ&usqp=CAU",
            "https://globalnews.ca/wp-content/uploads/2018/12/Abby-otter-thicc.jpg?quality=85&strip=all&w=720&h=379&crop=1",
            "https://www.calparks.org/sites/default/files/2019-09/iStock-1059316898_0.jpg",
            "https://i.guim.co.uk/img/media/76c3d4490e882c62c7d2eae593426da1da8d0d0f/0_418_4800_2879/master/4800.jpg?width=1200&quality=85&auto=format&fit=max&s=499a5a77abf39f360778cc08700178aa"
        ]
        index = random.randrange(0, len(links))
        embed = discord.Embed(title="Otter", description="a picture of an Otter")
        embed.set_image(url=links[index])
        await ctx.send(embed=embed)

    @commands.command(aliases=['memes', 'reddit'])
    async def meme(self, ctx):
        """sends a meme"""
        embed = discord.Embed(title="here's a meme", description="from r/memes")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 50)]['data']['url'])
                await ctx.send(embed=embed)

    @commands.command(aliases=['toast', 'burn'])
    async def roast(self, ctx, member: discord.Member):
        """roast's the mentioned member"""
        if f"{member.id}" in server_data[ctx.guild.id]['pussies']:
            await ctx.send(f"{member.mention}'s pretty cool!")
        roasts = [
            f"{member.mention}'s GPA may be high but the number of bitches on their dick is low",
            f"I would roast {member.mention}, but my mom said I shouldnt burn trash",
            f"I wish I could meet {member.mention} again and walk away this time",
            f"whoever told {member.mention} to be themselves was lying",
            f"sorry i can't think of an insult dumb enough for {member.mention} to understand",
            f"i would call {member.mention} an idiot but that would be an insult to stupid people",
            f"No breath mint can obscure the sheer stench of the bullshit that just came out of {member.mention}'s mouth just now."
        ]
        index = random.randrange(0, len(roasts))
        await ctx.send(roasts[index])

    @commands.command(aliases=['funni', 'funny', 'dadjoke', 'dad'])
    async def joke(self, ctx):
        """sends a random dad joke"""
        jokes = [
            'Why did the football coach go to the bank? To get his quarter back.',
            'Why cant a leopard hide? Hes always spotted.',
            'Air used to be free at the gas station, now it costs 2.50. You want to know why? Inflation.',
            'I tried to get a smart car the other day but they sold out too fast. Why? I guess Im just a bit slow.',
            'I told my wife that a husband is like a fine wine: we just get better with age. The next day she locked me in the cellar.',
            "Why does a husband lead a dog's life? He comes in with muddy feet, gets comfortable by the fire, and waits to be fed.",
            "Did you hear about the claustrophobic astronaut? He just wanted a bit more space.",
            "What does the stork do once he's delivered the baby? He lies on the couch and drinks a beer!",
            "How many telemarketers does it take to change a light bulb? Only one, but he has to do it during dinner.",
            "Why did the orange lose the race? It ran out of juice.",
            "How you fix a broken pumpkin? With a pumpkin patch.",
            "Why are fish so smart? They live in schools!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
            "Why did the man fall down the well? Because he couldn’t see that well!",
            "Why do peppers make such good archers? Because they habanero.",
            "What did the sink tell the toilet? You look flushed!",
            "why was the ant confused? because all of his undles were aunts!"
            "i asked my german friend what the square root of 81 was. he said no."
        ]
        index = random.randrange(0, len(jokes))
        await ctx.send(jokes[index])

    @commands.command(aliases=['ducky', 'ducks', 'quack'])
    async def duck(self, ctx):
        """sends a picture of a duck"""
        links = [
            "https://c.tenor.com/AQecc2g8uuAAAAAC/duck-dance.gif",
            "https://c.tenor.com/xxeMW4g1NTAAAAAC/duck-dancing-duck.gif",
            "https://upload.wikimedia.org/wikipedia/commons/a/a1/Mallard2.jpg",
            "https://www.thespruce.com/thmb/t13CIs9CH0HfuggdQ-DU9zk_QHo=/3780x2126/smart/filters:no_upscale()/do-ducks-have-teeth-4153828-hero-9614a7e9f4a049b48e8a35a9296c562c.jpg",
            "https://www.cnet.com/a/img/C4R_F8PD965L7Eakym2BWbk3O6s=/1200x630/2019/01/09/e30a81d2-f4e7-4439-98bf-61e288e16007/gettyimages-1045983738-1.jpg",
            "https://cdn.vox-cdn.com/thumbor/Wd-2zsFlWxXz1HgmGEEwXx5iYBI=/0x0:1000x605/1200x800/filters:focal(420x223:580x383)/cdn.vox-cdn.com/uploads/chorus_image/image/48780381/duck.0.png",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTn-GmO6ktjq8lB8zWnn8bEZzPK00gD7skuVg&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7qbhatJNmhUe9ZqRhEo1IgB5I_bnkrjCX7Q&usqp=CAU",
            "https://i.guim.co.uk/img/media/e0a3aa9884c7ff7e4a2a4351b6a5340e72368f0a/0_184_720_432/master/720.jpg?width=1200&quality=85&auto=format&fit=max&s=b47eed5571c5072dc81bef6cd70adf91",
        ]
        index = random.randrange(0, len(links))
        embed = discord.Embed(title="Duck", description="a picture of a duck")
        embed.set_image(url=links[index])
        await ctx.send(embed=embed)

    @commands.command(aliases=['kitty', 'katze'])
    async def cat(self, ctx):
        """sends a cat picture"""
        links = [
            "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/cute-cat-photos-1593441022.jpg?crop=0.669xw:1.00xh;0.166xw,0&resize=640:*",
            "https://images.unsplash.com/photo-1529778873920-4da4926a72c2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8Y3V0ZSUyMGNhdHxlbnwwfHwwfHw%3D&w=1000&q=80",
            "https://filmdaily.co/wp-content/uploads/2020/04/cute-cat-videos-lede-1300x882.jpg",
            "https://st1.latestly.com/wp-content/uploads/2021/08/31-6-784x441.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxXwz_aEcFGuXxbZx_vtCm3oIjpmO4Wmljug&usqp=CAU",
            "https://c.tenor.com/yheo1GGu3FwAAAAM/rick-roll-rick-ashley.gif",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgQZsLeDJcyOkhxr6ePwiBTla8YgljqFrIIw&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQuQl3_fbyN6nylNXIQ3N0L8Un_qTqVQ2VFRw&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNoFoDT2i40xTf9bAQbgL4YLQewb-4bSt6CA&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpdbrLlhVnaa0wldvuZqbF9dTSLz67HBAR4A&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbi0nRsf_MXf9LShlNY6vRMEgisddL-tBcoA&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7AdwCXShyDM6ZvcKFCTy898b_KKF7BCxdzQ&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSI5zoJRBJCAndOV13vCPQb1F_E4Zsg_zSu7w&usqp=CAU",
        ]
        index = random.randrange(0, len(links))
        embed = discord.Embed(title="Cat", description="a picture of a cat")
        embed.set_image(url=links[index])
        await ctx.send(embed=embed)

    @commands.command(aliases=['puppy', 'doggy', 'hund', 'hunden'])
    async def dog(self, ctx):
        """sends a dog picture"""
        links = [
            "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=1.00xw:0.669xh;0,0.190xh&resize=1200:*",
            "http://cdn.akc.org/content/article-body-image/golden_puppy_dog_pictures.jpg",
            "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8ZG9nc3xlbnwwfHwwfHw%3D&w=1000&q=80",
            "https://post.medicalnewstoday.com/wp-content/uploads/sites/3/2020/02/322868_1100-800x825.jpg",
            "https://ggsc.s3.amazonaws.com/images/uploads/The_Science-Backed_Benefits_of_Being_a_Dog_Owner.jpg",
            "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/smartest-dog-breeds-1553287693.jpg?crop=0.673xw:1.00xh;0.167xw,0&resize=640:*",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT36OGUq8X23zUYSRF3TEcQCcZbxdZvIphwcQ&usqp=CAU",
            "https://www.hemeltoday.co.uk/webimg/b25lY21zOjE0MWMyMWM1LTE5MTItNDZlYy1hMjljLTAxNGUwMGM4N2Y1YTo4ZjVmMjQ2Mi02M2Q2LTQ2YzEtOWZmMS1jY2ZjOWI5NmE3YmM=.jpg?width=640&enable=upscale",
            "https://cdn.britannica.com/q:60/49/161649-050-3F458ECF/Bernese-mountain-dog-grass.jpg",
            "https://www.guidedogs.org/wp-content/uploads/2021/11/01.11.2021_SGD1014-Edit-scaled.jpg",
            "https://images.unsplash.com/photo-1611003228941-98852ba62227?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8YmFieSUyMGRvZ3xlbnwwfHwwfHw%3D&w=1000&q=80",
            "https://hips.hearstapps.com/ghk.h-cdn.co/assets/16/08/gettyimages-464163411.jpg",
            "https://media.nature.com/lw800/magazine-assets/d41586-020-03053-2/d41586-020-03053-2_18533904.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxYy4mS5E0-eG5aKeoTPTtkwal628dGFsrgA&usqp=CAU",
        ]
        index = random.randrange(0, len(links))
        embed = discord.Embed(title="Dog", description="a picture of a dog")
        embed.set_image(url=links[index])
        await ctx.send(embed=embed)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(fun(bot))