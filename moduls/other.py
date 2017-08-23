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
        eg. .status Discord"""

        args = ' '.join(args)
        await self.bot.change_presence(game = discord.Game(name='%s' % args))

    async def on_member_join(self, member):
        server = member.server
        fmt = 'Welcome {0.mention} to {1.name}!'
        await self.bot.send_message(server, fmt.format(member, server))

    async def on_member_leave(self, member):
        server = member.server
        fmt = 'Farewell, {0.mention} !'
        await self.bot.send_message(server, fmt.format(member))
    
    def check_if_it_is_me(ctx):
        return ctx.message.author.name == "anto"

    @commands.command(pass_context=True, hidden = True)
    @commands.check(check_if_it_is_me)
    async def tg(self, ctx, name = "Johnnyeco", count = 1):
        channel = ctx.message.channel
        counter = 0
        async for message in self.bot.logs_from(channel, limit=100):
            if message.author.name == name:
                counter+=1
                if counter <= count:
                    await self.bot.delete_message(message)
            
        await self.bot.send_message(channel,'Be a nice doggo!')

def setup(bot):
    b = Other(bot)
    bot.add_listener(b.on_member_join,"on_member_join")
    bot.add_listener(b.on_member_leave,"on_member_leave")
    bot.add_cog(Other(bot))