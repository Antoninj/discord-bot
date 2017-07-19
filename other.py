import discord
import asyncio
from discord.ext import commands

import random
from random import randint

import aiohttp

class Other:
    """General purpose commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load(self, extension_name : str):
        """Loads an extension."""
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await self.bot.say("{} loaded.".format(extension_name))

    @commands.command()
    async def unload(self, extension_name : str):
        """Unloads an extension."""
        self.bot.unload_extension(extension_name)
        await self.bot.say("{} unloaded.".format(extension_name))

    @commands.command()
    async def status(self, *args):
        """Change Nestor status
        Nestor will change its status in Discord.      
        eg. *status Discord"""

        args = ' '.join(args)
        await self.bot.change_presence(game = discord.Game(name='%s' % args))


def setup(bot):
    bot.add_cog(Other(bot))