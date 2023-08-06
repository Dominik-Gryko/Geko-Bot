import discord
from discord.ext import commands
from datetime import datetime
import random

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name = "ping", description = "Will output the latency of the bot. Plus a Pong!") #commands need this decorator
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! {bot_latency} ms.")

        dateTime = datetime.now()
        print(f"{ctx.author.name} pinged {bot_latency} ms. at {dateTime:%d.%m.%Y %H:%M}")
    
    @commands.hybrid_command(name = "roll", description = "roll a dice to get a random integer.")
    async def roll(self, ctx):
        roll_dice = random.randint(1,6)

        my_filename = f'./cogs/png/Dice_{roll_dice}.png'
        with open(my_filename, "rb") as fh:
            f = discord.File(fh, filename=my_filename)

        if "-" in ctx.message.content: await ctx.message.delete()

        await ctx.send(f"{ctx.author.mention} rolled a {roll_dice}", file=f)
        await print(f"{ctx.author.name} rolled a {roll_dice}")

    @commands.command(name= "youtube" , aliases = ["yt"])
    async def youtube(self, ctx):
        link = "https://www.youtube.com/"
        await ctx.send(link)
        await print(f"{ctx.author.name} requested youtube link.")

    @commands.command(name = "tripaloski", aliases = ["tri", "paloski"])
    async def tripaloski(self, ctx):
        link = "https://www.youtube.com/watch?v=x7W8Y_g3W1s&ab_channel=jukkeboy"
        await ctx.send(link)
        await print(f"{ctx.author.name} requested tripaloski link.")
    
    @commands.command(name = "nanofly")
    async def nanofly(self, ctx):
        link = "https://nanoflystore.com/"
        await ctx.send(link)
        await print(f"{ctx.author.name} requested nanoflystore.")

    @commands.command(name = "johncena")
    async def johncena(self, ctx):
        cena = """
Imagine John Cena, the professional wrestler, 
sitting atop a giant hot dog. He's straddling the hot dog as if it were a horse. 
John Cena's iconic muscular physique contrasts with the whimsical nature of the scene. 
He has a determined and confident expression on his face as he "rides" the hot dog with his hands gripping its bun, almost as if he's in the middle of a wrestling match. 
The hot dog itself is larger than life, with a bright yellow mustard streak along its length and a line of ketchup as if it were a racing stripe. 
The whole scene is a playful and humorous portrayal, capturing the larger-than-life personality of John Cena and the imaginative concept of him riding a hot dog.
"""

        await ctx.send(cena + "https://www.cultofwhatever.com/wp-content/uploads/2016/02/gif-john-cena-eyebrows.gif")
        
async def setup(bot):
    await bot.add_cog(fun(bot))