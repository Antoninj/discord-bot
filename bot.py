import discord
import asyncio
from discord.ext import commands
import logging
import random
from random import randint

# Logging config
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

Nestor = commands.Bot(command_prefix='.', description="Nestor, at your service.")


@Nestor.event
async def on_ready():
    print('Logged in as')
    print(Nestor.user.name)
    print(Nestor.user.id)

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



if __name__=="__main__":

    # Bot token
    with open("bot_token.txt","r") as file:
        TOKEN = file.read()

    # This specifies what extensions to load when the bot starts up
    startup_extensions = ["music", "other", "game", "fun", "chat"]

    # Load startup extensions
    for extension in startup_extensions:
        try:
            Nestor.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    # Run the bot
    Nestor.run(TOKEN)


