import discord
import asyncio
from discord.ext import commands
import chatterbot

from PIL import Image
from io import BytesIO
from lxml import html

import random
from random import randint,choice

import aiohttp

class Fun:
    """Fun commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def horoscope(self, sign : str):
        """Horoscope
        Nestor will tell you your daily horoscope based on your astrological sign.
        eg. *horoscope leo"""

        url = 'http://horoscope-api.herokuapp.com/horoscope/today/{}'.format(sign)

        async with aiohttp.request('GET',url) as horoscope_api:
            data  = await horoscope_api.json()
            horoscope  = data["horoscope"].replace("\\r\\n ","").replace("[","").replace("]","").replace("'","").strip()

            await self.bot.say(horoscope)

    @commands.command()
    async def speak(self,*text : str):
        """Text to speech 
        Nestor will speak out loud what you wrote.
        eg. *speak hello"""
        await self.bot.say(" ".join(text), tts=True)

    @commands.command(pass_context=True)
    async def love(self, ctx , name1: str, name2 : str):
        """Show % of affinity between 2 persons
        Nestor will tell you if you are compatible with someone else.
        eg. *love lise"""

        api_key = "icgNGtioNNmshqOQuh3nPYSOcmo3p1eV3pHjsnTtNXTLiC0pot"
        payload = {"fname": name1, "sname" : name2}
        headers={ "X-Mashape-Key": "icgNGtioNNmshqOQuh3nPYSOcmo3p1eV3pHjsnTtNXTLiC0pot", "Accept": "text/plain"}

        url = 'https://love-calculator.p.mashape.com/getPercentage'

        async with aiohttp.request('GET',url, params = payload , headers = headers) as resp:
            data  = await resp.json()
            response  = "Affinity percentage: {}%. {}".format(data['percentage'],data['result'])
            await self.bot.say(response)

    @commands.command(pass_context=True)
    async def robot(self, ctx , text: str):
        """ Get a robot image from text
        Nestor will generate a robot image base on the text input.
        eg. *robot antonin"""

        url = 'https://robohash.org/{}'.format(text)

        async with aiohttp.request('GET',url) as resp:
            data  = await resp.read()
            
            img = Image.open(BytesIO(data))
            img.save("data/images/img.png")

            await self.bot.upload('data/images/img.png')


    @commands.command()
    async def yoda(self, *sentence : str):
        """Speak like yoda
        Nestor will change your sentence to a yoda fashion.
        eg. *yoda You are young and dumb."""

        api_key = "icgNGtioNNmshqOQuh3nPYSOcmo3p1eV3pHjsnTtNXTLiC0pot"
        payload = {"sentence":' '.join(sentence)}
        headers={ "X-Mashape-Key": "icgNGtioNNmshqOQuh3nPYSOcmo3p1eV3pHjsnTtNXTLiC0pot", "Accept": "text/plain"}

        url = 'https://yoda.p.mashape.com/yoda'
        async with aiohttp.request('GET',url, params = payload , headers = headers) as resp:
            await self.bot.say(await resp.text())

    @commands.command()
    async def penis(self, *, user : discord.Member):
        """Detects user's penis length
        This is 100% accurate."""
        state = random.getstate()
        random.seed(user.id)
        dong = "8{}D".format("=" * random.randint(5, 30))
        random.setstate(state)
        await self.bot.say("Size: " + dong )


    @commands.command()
    async def quotes(self, count : int = None):
        """Random quotes
        Nestor will provide you with a random quotation.
        eg. *quotes"""

        api_key = "icgNGtioNNmshqOQuh3nPYSOcmo3p1eV3pHjsnTtNXTLiC0pot"
        categories = ["movies","famous"]

        if count is None: 
            count = 1

        payload = {"cat":random.choice(categories),'count' : count}
        headers={ "X-Mashape-Key": "icgNGtioNNmshqOQuh3nPYSOcmo3p1eV3pHjsnTtNXTLiC0pot", 
        "Accept": "text/plain"}

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
        eg. *coinflip"""

        coinflip = ['Heads!', 'Tails!']
        await self.bot.say(random.choice(coinflip))


    @commands.command()
    async def fml(self):
        """ Fuck my life
        Nestor will tell you a random fuck my life sentence.
        eg. *fml"""

        url = 'https://www.fmylife.com/random'

        async with aiohttp.request('GET',url) as fml_website:
            data  = await fml_website.text()
            tree = html.fromstring(data)
            fml_text= tree.xpath('//p[@class="block hidden-xs"]/a/text()')
            fml = choice(fml_text)
            await self.bot.say(fml)


def setup(bot):
    bot.add_cog(Fun(bot))