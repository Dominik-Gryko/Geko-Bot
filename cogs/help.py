import discord
from discord.ext import commands


helplist = """
```
General commands:
-help - displays all the available commands for thy bot
-ping - will respond with the bots latency in ms.
-roll - will roll a "dice", responds with a random number between 1 and 6.

Admin Commands:
 ban <@member> <reason> - will ban the @ member with a reason/with no reason.
 kick <@member> <reason> - will kick the @ member with a reason/with no reason.
 clear <amount of messages> - will delete the amount of messages specified.
 unban <userid> - will unban a member using their userid.
 mute - will time someone out.
 goodbye - goodbye setup embed.
 welcome - welcome setup embed.
 logging - logging setup embed.
```
"""



class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name = "help", aliases = ["h" , "hlp", "hel"])
    async def Help(self, ctx):
        await ctx.send(helplist)
        await print(f"{ctx.author.name} requested for a help message!")


async def setup(bot):
    await bot.add_cog(help(bot))