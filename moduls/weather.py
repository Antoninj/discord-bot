import discord
import asyncio
from discord.ext import commands
import aiohttp
import json

# Load configuration file for the bot
with open("config/config.json") as cfg:
    config = json.load(cfg)

# Load city info file
with open("data/weather/city.list.json") as city_info:
    city_data = json.load(city_info)

API_KEY = config["open_weather_api_key"]

class Weather:
    """Weather forecast commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, *location_name : str):
         """ weather forecast
         Nestor will show the weather forecast for a specific location.
         eg. .weather paris
        """
        if location_name:
            location_name = "+".join(keywords)
            location_id = self.get_location_id(location_name)

        else:
            await self.bot.say("Please enter a location to get the weather forecast.")
            return
        
        url = "http://api.openweathermap.org/data/2.5/weather?id={}&APPID={}".format(location_id,API_KEY)
            async with aiohttp.request('GET',url) as weather_request:
                weather_data  = await weather_request.json()
                print(weather_data)

    def get_location_id(location_name):
        location_id = 1
        return location_id

def setup(bot):
     # Set up background tasks
    bot.add_cog(Weather(bot))
