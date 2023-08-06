import discord
from discord.ext import commands
import asyncio
import datetime
import json


class member_management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @commands.Cog.listener()
    async def on_message(self, message): #WORD_FILTER
        with open("./cogs/json/word_filter.json", "r") as f:
            data = json.load(f)
        
        enabled = data[str(message.guild.id)]["Enabled"]
        if (enabled == None) or (enabled == False): return
        
        banned_words = data[str(message.guild.id)]["Banned_Words"]
        for word in banned_words:
            if word in message.content.lower() or word in message.content.upper():
                await message.delete()
                await message.channel.send(f"{message.author.mention}, You cant use that word!")
    
    
    @commands.hybrid_command(name = "clear", aliases = ["clr", "c"], description = "clear an amount of messages")
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, count: int):
        await ctx.channel.purge(limit = count)
        channel_name = ctx.channel.name
        await print(f"{ctx.author.name} deleted {count} message(s) in {channel_name}.")
    
    @commands.hybrid_command(name = "kick", aliases = ["k", "remove"], description = "kick someone that is misbehaving or someone you dont like.")
    @commands.has_permissions(kick_members=True, manage_messages = True)
    async def kick(self, ctx, member:discord.Member, *, reason = None):
        await ctx.channel.purge(limit = 1)
        await ctx.guild.kick(member)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name = "Kicked: ", value = f"{member.mention} has been kicked from the server by {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name = "Reason: ", value = reason, inline = False)

        await ctx.send(embed=conf_embed)
        await print(f'{ctx.author.name} kicked {member.name} for "{reason}"')

    @commands.hybrid_command(name="ban", aliases = ["b", "Ban", "BAN", "Terminate", "Banish"], description = "Banish someone from thy guild due to any reason, or none.")
    @commands.has_permissions(ban_members = True, manage_messages = True)
    async def ban(self, ctx, member:discord.Member, *, reason = None):
        await ctx.channel.purge(limit = 1)
        await ctx.guild.ban(member)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name = "Kicked: ", value = f"{member.mention} has been banned from the server by {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name = "Reason: ", value = reason, inline = False)

        await ctx.send(embed = conf_embed)
        await print(f'{ctx.author.name} banned {member.name} for "{reason}"')
    

    @commands.hybrid_command(name="unban", aliases = ["unb"], description = "Unbanish someone from thy guild due to any reason, or none.")
    @commands.guild_only()
    @commands.has_permissions(ban_members = True, manage_messages = True)
    async def unban(self, ctx, userid):
        user = discord.Object(id = userid)
        await ctx.channel.purge(limit = 1)
        await ctx.guild.unban(user)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name = "Kicked: ", value = f"<@{userid}> has been unbanned from the server by {ctx.author.mention}.", inline=False)

        await ctx.send(embed = conf_embed)
        await print(f'{ctx.author.name} unbanned {userid}')

    @commands.hybrid_command(name = "mute", aliases = ["timeout"], description= "Mute/Timeout someone for a certain amount of time.")
    @commands.has_permissions(moderate_members= True)
    async def timeout(self, ctx, member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, weeks: int = 0, reason: str = None):
        duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days, weeks=weeks)
        await member.timeout(duration, reason=reason)
        await ctx.response.send_message(f"{member.mention} has been muted until <t:{duration}:R>.")

    
    @commands.command(name = "userinfo")
    @commands.has_permissions(administrator = True)
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        elif member is not None:
            member = member
        
        info_embed = discord.Embed(title=f"{member.name}'s User Information", description="All information about this user.", color = member.color)
        info_embed.set_thumbnail(url = member.avatar)
        info_embed.add_field(name="Name:", value=member.name, inline=False)
        info_embed.add_field(name="Nickname:", value=member.display_name, inline=False)
        info_embed.add_field(name="ID:", value=member.id, inline=False)
        info_embed.add_field(name="Top Role:", value=member.top_role, inline=False)
        info_embed.add_field(name="Status:", value=member.status, inline=False)
        info_embed.add_field(name="Bot user?:", value=member.bot, inline=False)
        info_embed.add_field(name="Account Creation Date:", value=member.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"), inline=False)

        await ctx.send(embed = info_embed)

async def setup(bot):
    await bot.add_cog(member_management(bot))
    
