import discord
import asyncio
from discord.ext import commands
import logging
import random
from lxml import html

import random
from random import randint,choice

import aiohttp

# Logging config
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='log/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

Nestor = commands.Bot(command_prefix=commands.when_mentioned_or('.'), description="Nestor, at your service.")


@Nestor.event
async def on_ready():
    print('Logged in as :')
    print(Nestor.user.name)
    print(Nestor.user.id)
    await Nestor.change_presence(game = discord.Game(name=".help for commands"))

@Nestor.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await Nestor.send_message(server, fmt.format(member, server))

@Nestor.command(pass_context=True, hidden = True)
async def tg(ctx, name = "Johnnyeco", count = 1):
    channel = ctx.message.channel
    if ctx.message.author.name == "anto":
        counter = 0
        async for message in Nestor.logs_from(channel, limit=100):
            if message.author.name == name:
                counter+=1
                if counter <= count:
                    await Nestor.delete_message(message)
        
        await Nestor.send_message(channel,'Be a nice doggo !')

    else:
        await Nestor.send_message(channel, "Sorry, I don't take orders from you ...")

async def fml_background_task():
    await Nestor.wait_until_ready()
    channels = Nestor.get_all_channels()
    channels_ids = [channel.id for channel in channels if channel.name == "general" and channel.type is discord.ChannelType.text]

    count = 0
    while not Nestor.is_closed:
        if count % 2 == 0:
            url = 'https://www.fmylife.com/random'
        else:
            url = "http://www.viedemerde.fr/aleatoire"

        async with aiohttp.request('GET',url) as fml_website:
            data  = await fml_website.text()
            tree = html.fromstring(data)
            fml_text= tree.xpath('//p[@class="block hidden-xs"]/a/text()')
            fml = choice(fml_text)

        for id in channels_ids[:2]:
            channel = Nestor.get_channel(id)
            await Nestor.send_message(channel, fml)
        await asyncio.sleep(7200) # task runs every 2 hours

        count+=1

"""
@Nestor.event
async def on_message(message):

    insults = ["Cool story, bro","I'd love to stop and chat to you but I'd rather have type 2 diabetes.",
    "Fascinating story, in what chapter do you shut the fuck up?","I give zero fucks.",
    "Looking for a fuck to give.","I don't give a flying fuck.","You Fucktard!",
    "Fuck you very much.","Please go fuck yourself","Maybe. Maybe not. Maybe fuck yourself.",
    "Please choke on a bucket of cocks.","Eat a bag of fucking dicks."]

    if message.author == Nestor.user:
        return
    elif message.author.name == "notdiddin":
        await Nestor.send_message(message.channel, random.choice(insults))
        return
    else:
        await Nestor.process_commands(message)
        
"""


if __name__=="__main__":

    # Bot token
    with open("bot_token.txt","r") as file:
        TOKEN = file.read()

    # This specifies what extensions to load when the bot starts up
    startup_extensions = ["other", "game", "fun", "image", "music", "trivia", "economy"]

    # Load startup extensions
    for extension in startup_extensions:
        try:
            extension = "moduls."+ extension
            Nestor.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    # Set up background tasks
    #Nestor.loop.create_task(fml_background_task())

    # Run the bot
    Nestor.run(TOKEN)


