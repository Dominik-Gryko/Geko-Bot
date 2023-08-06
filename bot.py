import discord
from discord.ext import commands
import os
import asyncio
from termcolor import cprint
import json


intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="-", intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="-help | Geko-bot"))
    cprint(f"Success: {bot.application.name} is connected to Discord", 'blue')

def load_from_json(filename):
    with open(f"./cogs/json/{filename}", 'r') as f:
        data = json.loads(f.read()) 
        return data

def json_guild_setup(filename, guild, fields = []):
    data = load_from_json(filename)

    data[str(guild)] = {}
    for field in fields:
        data[str(guild)][field] = None
    
    with open(f"cogs/json/{filename}", "w") as f:
        data = json.dump(data, f, indent=4)
    

def json_guild_remove(filename, guild):
    data = load_from_json(filename)
    data.pop(str(guild))
    with open(f"cogs/json/{filename}", "w") as f:
        data = json.dump(data, f, indent=4)


def download_github_file(raw_link, filepath = None):
    import requests 
    response = requests.get(raw_link)
    if filepath == None: print("Need to enter filepath aswell.")
    
    with open(filepath, "wb") as f:
        f.write(response.content)

def check_and_create_file(filepath, data = None):
    if not os.path.exists(filepath):
        if data is None: data = {}
        with open(filepath, "w") as f:
            json.dump(data, f)
    else: pass

def check_and_download_file(url, filepath):

    if not os.path.exists(filepath):
        download_github_file(url, filepath)

def check_and_create_directory(mypath):
    if not os.path.isdir(mypath):
        os.makedirs(mypath)

async def setup():

    data = load_from_json("settings.json")

    token = input("Enter your token (this token will be saved in settings.json): ")
    data["token"] = token
 
    with open(f"cogs/json/settings.json", "w") as f:
        data = json.dump(data, f, indent=4)    
        cprint("Success: Token has been saved", "green")

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def files_presence_check():
    check_and_create_directory("./cogs")
    check_and_download_file("https://raw.githubusercontent.com/Dominik-Gryko/Geko-Bot/main/cogs/fun.py", "./cogs/fun.py")
    check_and_download_file("https://raw.githubusercontent.com/Dominik-Gryko/Geko-Bot/main/cogs/help.py", "./cogs/help.py")
    check_and_download_file("https://raw.githubusercontent.com/Dominik-Gryko/Geko-Bot/main/cogs/logging.py", "./cogs/logging.py")
    check_and_download_file("https://raw.githubusercontent.com/Dominik-Gryko/Geko-Bot/main/cogs/moderation.py", "./cogs/moderation.py")
    check_and_download_file("https://raw.githubusercontent.com/Dominik-Gryko/Geko-Bot/main/cogs/welcome_goodbye.py", "./cogs/welcome_goodbye.py")
    
    check_and_create_directory("./cogs/json")
    check_and_create_file("./cogs/json/welcome.json")
    check_and_create_file("./cogs/json/goodbye.json")
    check_and_create_file("./cogs/json/logging.json")
    check_and_create_file("./cogs/json/word_filter.json")
    settings_data = {
        "token": None,
        "reconnect": False,
    }
    check_and_create_file("./cogs/json/settings.json", settings_data)

    check_and_create_directory("./cogs/png")
    for i in range(1, 7):
        check_and_download_file(f"https://raw.githubusercontent.com/Dominik-Gryko/Geko-Bot/main/cogs/png/Dice_{i}.png", f"./cogs/png/dice_{i}.png")
    

@bot.event
async def on_guild_join(guild):
    guildID = str(guild.id)
    
    json_guild_setup("welcome.json", guildID, fields = ["Channel", "Message", "AutoRole", "ImageUrl"])
    json_guild_setup("goodbye.json", guildID, fields = ["Channel"])
    json_guild_setup("logging.json", guildID, fields = ["Channel"])
    json_guild_setup("word_filter.json", guildID, fields = ["Enabled", "Banned_Words"])


@bot.event
async def on_guild_remove(guild):
    guildID = str(guild.id)

    json_guild_remove("welcome.json", guildID)
    json_guild_remove("goodbye.json", guildID)
    json_guild_remove("logging.json", guildID)
    json_guild_remove("word_filter.json", guildID)


async def main():
    async with bot:
        await files_presence_check()
        await load_cogs() 

        settings = load_from_json("settings.json")
        if settings["token"] is None: 
            await setup()
            settings = load_from_json("settings.json")

        try:
            await bot.start(settings['token'], reconnect = settings['reconnect'])

        except Exception as e:
            cprint(e, "red")

asyncio.run(main())