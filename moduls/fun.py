import discord
import asyncio
from discord.ext import commands
from lxml import html
import random
from random import randint,choice
import aiohttp
import json

# Load configuration file for the bot
with open("config/config.json") as cfg:
    config = json.load(cfg)

API_KEY = config["mashape_api_key"]

class Fun:
    """A bunch of (hopefully) fun commands to keep you entertained
    """
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.fml_background_task(7200)) # task runs every even hour
        self.bot.loop.create_task(self.quotes_background_task(3600)) # task runs every odd hour

    @commands.command()
    async def horoscope(self, sign : str):
        """Horoscope
        Nestor will tell you your daily horoscope based on your astrological sign.
        eg. .horoscope leo"""
        url = 'http://horoscope-api.herokuapp.com/horoscope/today/{}'.format(sign)
        async with aiohttp.request('GET',url) as horoscope_api:
            data  = await horoscope_api.json()
            #print(data["horoscope"])
            horoscope  = data["horoscope"].replace("\\r\\n","").replace("[","").replace("\\n","").replace("]","").replace("'","").strip()
            await self.bot.say(horoscope)

    @commands.command()
    async def speak(self,*text : str):
        """Text to speech 
        Nestor will speak out loud what you wrote.
        eg. .speak hello"""
        await self.bot.say(" ".join(text), tts=True)

    @commands.command(pass_context=True)
    async def love(self, ctx , name1: str, name2 : str):
        """Show % of affinity between 2 persons
        Nestor will tell you if you are compatible with someone else.
        eg. .love john lise"""
        payload = {"fname": name1, "sname" : name2}
        headers={ "X-Mashape-Key": API_KEY, "Accept": "text/plain"}
        url = 'https://love-calculator.p.mashape.com/getPercentage'
        async with aiohttp.request('GET',url, params = payload , headers = headers) as resp:
            data  = await resp.json()
            response  = "Affinity percentage: {}%. {}".format(data['percentage'],data['result'])
            await self.bot.say(response)

    @commands.command()
    async def yoda(self, *sentence : str):
        """Speak like yoda
        Nestor will change your sentence to a yoda fashion.
        eg. .yoda You are young and dumb."""
        payload = {"sentence":' '.join(sentence)}
        headers={ "X-Mashape-Key": API_KEY, "Accept": "text/plain"}
        url = 'https://yoda.p.mashape.com/yoda'
        async with aiohttp.request('GET',url, params = payload , headers = headers) as resp:
            await self.bot.say(await resp.text())

    @commands.command()
    async def penis(self, *, user : discord.Member):
        """Detects user's penis length
        This is 100% accurate.
        eg .penis @user"""
        state = random.getstate()
        random.seed(user.id)
        dong = "8{}D".format("=" * random.randint(5, 30))
        random.setstate(state)
        await self.bot.say("Size: " + dong )

    @commands.command()
    async def quotes(self, count : int = 1):
        """Random quotes
        Nestor will provide you with a random quotation.
        eg. .quotes"""
        categories = ["movies","famous"]
        payload = {"cat":random.choice(categories),'count' : count}
        headers={ "X-Mashape-Key": API_KEY, "Accept": "text/plain"}
        url = 'https://andruxnet-random-famous-quotes.p.mashape.com/'
        async with aiohttp.request('GET',url, params = payload , headers = headers) as resp:

            data  = await resp.json()
            if count >1:
                quotes = [quote["quote"] for quote in data]
                authors = [quote["author"] for quote in data]
                
            else:
                quotes = [data["quote"]]
                authors = [data["author"]]

            zipped = list(zip(quotes,authors))
            curated  = [" ".join(item) for item in zipped]
            sentence = '\n'.join(curated)

        await self.bot.say(sentence)

    @commands.command()
    async def coinflip(self, *coinflip : str):
        """Flip a coin
        Nestor will randomly choose between 'heads' or 'tails'.
        eg. .coinflip"""
        coinflip = ['Heads!', 'Tails!']
        await self.bot.say(random.choice(coinflip))

    @commands.command()
    async def fml(self):
        """ Fuck my life
        Nestor will tell you a random fuck my life sentence.
        eg. .fml"""
        url = 'https://www.fmylife.com/random'
        async with aiohttp.request('GET',url) as fml_website:
            data  = await fml_website.text()
            tree = html.fromstring(data)
            fml_text= tree.xpath('//p[@class="block hidden-xs"]/a/text()')
            fml = choice(fml_text)
            await self.bot.say(fml)

    async def fml_background_task(self, time : int):
        await self.bot.wait_until_ready()
        channels = self.bot.get_all_channels()
        channels_ids = [channel.id for channel in channels if channel.name == "bot-spam" and channel.type is discord.ChannelType.text]
        count = 0
        while not self.bot.is_closed:
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
                channel = self.bot.get_channel(id)
                await self.bot.send_message(channel, fml)
            await asyncio.sleep(time) 

            count+=1

    async def quotes_background_task(self, time : int, count : int = 1):
        categories = ["movies","famous"]
        payload = {"cat":random.choice(categories),'count' : count}
        headers={ "X-Mashape-Key": API_KEY, "Accept": "text/plain"}

        url = 'https://andruxnet-random-famous-quotes.p.mashape.com/'
        await self.bot.wait_until_ready()
        channels = self.bot.get_all_channels()
        channels_ids = [channel.id for channel in channels if channel.name == "bot-spam" and channel.type is discord.ChannelType.text]

        while not self.bot.is_closed:
            await asyncio.sleep(time) 

            async with aiohttp.request('GET',url, params = payload , headers = headers) as resp:

                data  = await resp.json()
                if count >1:
                    quotes = [quote["quote"] for quote in data]
                    authors = [quote["author"] for quote in data]
                    
                else:
                    quotes = [data["quote"]]
                    authors = [data["author"]]

                zipped = list(zip(quotes,authors))
                curated  = [" ".join(item) for item in zipped]
                sentence = '\n'.join(curated)
            for id in channels_ids[:2]:
                channel = self.bot.get_channel(id)
                await self.bot.send_message(channel, sentence)

            await asyncio.sleep(time) 

def setup(bot):
     # Set up background tasks
    bot.add_cog(Fun(bot))
