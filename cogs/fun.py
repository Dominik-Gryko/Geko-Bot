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
        
async def setup(bot):
    await bot.add_cog(fun(bot))