import discord
from discord.ext import commands
import json

class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.author.id == self.bot.user.id: return
        if message.author.bot == True: return
        if "-" in message.content: return
        
        
        with open("./cogs/json/logging.json", "r") as f:
            data = json.load(f)
        
        logging_channel = discord.utils.get(message.guild.channels, name=data[str(message.guild.id)]["Channel"])
        
        logging_embed = discord.Embed(title = "Message Logged", color = discord.Color.gold())
        logging_embed.add_field(name="Message Author:", value=message.author.mention, inline=False)
        logging_embed.add_field(name="Channel Origin:", value=message.channel.mention, inline=False)
        
        if message.content:
            logging_embed.add_field(name="Message Content:", value=message.content, inline=False)
        
        if message.attachments:
            attachments = message.attachments
            urls = []

            for attch in attachments: urls.append(attch.url)
            urls = str(urls).strip("[],")

            logging_embed.add_field(name = "Message Attatchments:", value = urls)

        if data[str(message.guild.id)]["Channel"] is not None:
            await logging_channel.send(embed = logging_embed)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("./cogs/json/logging.json", "r") as f:
            data = json.load(f)

        
        logging_channel = discord.utils.get(member.guild.channels, name=data[str(member.guild.id)]["Channel"])
        
        logging_embed = discord.Embed(title = "Arrival Logged", color = discord.Color.teal())
        logging_embed.add_field(name="Member Arrived:", value=member.mention, inline=False)

        if data[str(member.guild.id)]["Channel"] is not None:
            await logging_channel.send(embed = logging_embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open("./cogs/json/logging.json", "r") as f:
            data = json.load(f)
        

        logging_channel = discord.utils.get(member.guild.channels, name=data[str(member.guild.id)]["Channel"])
        
        logging_embed = discord.Embed(title = "Departure Logged", color = discord.Color.red())
        logging_embed.add_field(name="Member Departure:", value=f"<@{str(member.id)}>", inline=False)

        if data[str(member.guild.id)]["Channel"] is not None:
            await logging_channel.send(embed = logging_embed) 

    @commands.group(name = "logging", invoke_without_command=True)
    @commands.has_permissions(administrator = True)
    async def logging(self, ctx):

        info_embed = discord.Embed(title="Logging System Setup", description="Create a simple logging system for your server!", color = discord.Color.teal())
        info_embed.add_field(name = "channel", value="Set a channel for your logging message to be sent in.", inline=False)
        #info_embed.add_field(name = "message", value="Set a message to be included in your welcome card.", inline=False)

        await ctx.send(embed = info_embed)
        
    
    @logging.command()
    @commands.has_permissions(administrator = True)
    async def channel(self, ctx, channel:discord.TextChannel):

        with open("./cogs/json/logging.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["Channel"] = str(channel.name)

        with open("./cogs/json/logging.json", "w") as f:
            json.dump(data, f, indent = 4)


async def setup(bot):
    await bot.add_cog(logging(bot))
