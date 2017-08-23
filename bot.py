import discord
import asyncio
from discord.ext import commands
import logging
import random
from random import randint,choice
import json

# Logging config
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='log/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Load configuration file for the bot
with open("config/config.json") as cfg:
    config = json.load(cfg)
# Bot token
TOKEN = config['bot_token']

# This specifies what extensions to load when the Nestor starts up
startup_extensions = config['startup_extensions']

def startup(startup_extensions, bot):
    # Load startup extensions
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

def main():
    # Create an instance of the bot
    Nestor = commands.Bot(command_prefix=commands.when_mentioned_or('.'), description="Nestor, at your service.")

    @Nestor.event
    async def on_ready():
        print('Logged in as :')
        print(Nestor.user.name)
        print(Nestor.user.id)
        await Nestor.change_presence(game = discord.Game(name=".help for commands"))

    # Load startup extensions
    startup(startup_extensions, Nestor)

    # Run the bot
    Nestor.run(TOKEN)

if __name__=="__main__":
    main()

