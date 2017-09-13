from discord.ext import commands
from random import choice, shuffle,randint
import aiohttp
import functools
import PIL
from PIL import Image
from io import BytesIO
import asyncio
import json


try:
    from imgurpython import ImgurClient
except:
    ImgurClient = False

# Load configuration file for the bot
with open("config/config.json") as cfg:
    config = json.load(cfg)

CLIENT_ID = config["imgurclient_id"]
CLIENT_SECRET = config["imgurclient_secret"]
GIPHY_API_KEY = config["giphy_api_key"]
API_KEY = config["mashape_api_key"]



class Image:
    """Image related commands."""

    def __init__(self, bot):
        self.bot = bot
        self.imgur = ImgurClient(CLIENT_ID, CLIENT_SECRET)

    @commands.group(name="imgur", no_pm=True, pass_context=True)
    async def _imgur(self, ctx):
        """Retrieves pictures from imgur"""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Type **.help imgur** for subcommands information.")

    @_imgur.command(pass_context=True, name="random")
    async def imgur_random(self, ctx, *, term: str=None):
        """Retrieves a random image from Imgur
        Search terms can be specified"""
        if term is None:
            task = functools.partial(self.imgur.gallery_random, page=0)
        else:
            task = functools.partial(self.imgur.gallery_search, term,
                                     advanced=None, sort='time',
                                     window='all', page=0)
        task = self.bot.loop.run_in_executor(None, task)

        try:
            results = await asyncio.wait_for(task, timeout=10)
        except asyncio.TimeoutError:
            await self.bot.say("Error: request timed out")
        else:
            if results:
                item = choice(results)
                link = item.gifv if hasattr(item, "gifv") else item.link
                await self.bot.say(link)
            else:
                await self.bot.say("Your search terms gave no results.")

    @_imgur.command(pass_context=True, name="search")
    async def imgur_search(self, ctx, *, term: str):
        """Searches Imgur for the specified term and returns up to 3 results"""
        task = functools.partial(self.imgur.gallery_search, term,
                                 advanced=None, sort='time',
                                 window='all', page=0)
        task = self.bot.loop.run_in_executor(None, task)

        try:
            results = await asyncio.wait_for(task, timeout=10)
        except asyncio.TimeoutError:
            await self.bot.say("Error: request timed out")
        else:
            if results:
                shuffle(results)
                msg = "Search results...\n"
                for r in results[:3]:
                    msg += r.gifv if hasattr(r, "gifv") else r.link
                    msg += "\n"
                await self.bot.say(msg)
            else:
                await self.bot.say("Your search terms gave no results.")

    @_imgur.command(pass_context=True, name="subreddit")
    async def imgur_subreddit(self, ctx, subreddit: str, sort_type: str="top", window: str="day"):
        """Gets images from the specified subreddit section
        Sort types: new, top
        Time windows: day, week, month, year, all"""
        sort_type = sort_type.lower()

        if sort_type not in ("new", "top"):
            await self.bot.say("Only 'new' and 'top' are a valid sort type.")
            return
        elif window not in ("day", "week", "month", "year", "all"):
            await self.bot.send_cmd_help(ctx)
            return

        if sort_type == "new":
            sort = "time"
        elif sort_type == "top":
            sort = "top"

        links = []

        task = functools.partial(self.imgur.subreddit_gallery, subreddit,
                                 sort=sort, window=window, page=0)
        task = self.bot.loop.run_in_executor(None, task)
        try:
            items = await asyncio.wait_for(task, timeout=10)
        except asyncio.TimeoutError:
            await self.bot.say("Error: request timed out")
            return

        for item in items[:3]:
            link = item.gifv if hasattr(item, "gifv") else item.link
            links.append("{}\n{}".format(item.title, link))

        if links:
            await self.bot.say("\n".join(links))
        else:
            await self.bot.say("No results found.")

    @commands.command(pass_context=True, no_pm=True)
    async def gif(self, ctx, *keywords):
        """Retrieves first search result from giphy
        """
        if keywords:
            keywords = "+".join(keywords)
        else:
            await self.bot.say("Please enter a search term")
            return

        url = ("http://api.giphy.com/v1/gifs/search?&api_key={}&q={}"
               "".format(GIPHY_API_KEY, keywords))

        async with aiohttp.get(url) as r:
            result = await r.json()
            if r.status == 200:
                if result["data"]:
                    await self.bot.say(result["data"][0]["url"])
                else:
                    await self.bot.say("No results found.")
            else:
                await self.bot.say("Error contacting the API")

    @commands.command(pass_context=True, no_pm=True)
    async def gifr(self, ctx, *keywords):
        """Retrieves a random gif from a giphy search"""
        if keywords:
            keywords = "+".join(keywords)
        else:
            await self.bot.say("Please enter a search term")
            return

        url = ("http://api.giphy.com/v1/gifs/random?&api_key={}&tag={}"
               "".format(GIPHY_API_KEY, keywords))

        async with aiohttp.get(url) as r:
            result = await r.json()
            if r.status == 200:
                if result["data"]:
                    await self.bot.say(result["data"]["url"])
                else:
                    await self.bot.say("No results found.")
            else:
                await self.bot.say("Error contacting the API")
    
    # This needs to be debugged
    @commands.command(pass_context=True, hidden = True)
    async def cat(self,ctx):
        """Generate random cat picture"""
        headers={ "X-Mashape-Key": API_KEY, "Accept": "application/json"}
        url = 'https://nijikokun-random-cats.p.mashape.com/random'
        async with aiohttp.request('GET',url, headers = headers) as resp:
            data  = await resp.json()
            print(data)
            await self.bot.say(data["source"])
    
    '''
    @commands.command(pass_context=True)
    async def cat(self,ctx):
        """Generate random cat picture"""
        nbr = randint(1, 1000)
        url = "http://random.cat/view?i={}".format(nbr)
        async with aiohttp.request('GET',url) as resp:
            data  = await resp.json()
            print(data)
            #await self.bot.say(data["source"])
    '''

    @commands.command(pass_context=True)
    async def robot(self, ctx , *text: str):
        """ Get a robot image from text
        Nestor will generate a robot image base on the text input.
        eg. .robot antonin"""
        url = 'https://robohash.org/{}'.format("-".join(text))
        async with aiohttp.request('GET',url) as resp:
            data  = await resp.read() 
            img = PIL.Image.open(BytesIO(data))
            img.save("data/images/img.png")
            await self.bot.upload('data/images/img.png')


def setup(bot):
    if ImgurClient is False:
        raise RuntimeError("You need the imgurpython module to use this.\n"
                           "pip3 install imgurpython")

    bot.add_cog(Image(bot))