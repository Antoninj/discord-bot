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

    @commands.group(name="weather", pass_context=True)
    async def _weather(self, ctx):
        """Weather forecast related commands"""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Type **.help weather** for subcommands information.")

    @_weather.command(name="wind")
    async def weather_wind(self, *location_name : str):
         """ Shows wind strength 
         Nestor will show the wind forecast for a specific location.
         eg. .weather wind paris"""
         if location_name:
            location_ids = self.get_location_ids(location_name)

         else:
            await self.bot.say("Please enter a location to get the weather forecast.")
            return

         if len(location_ids) >0 :
             for location_id in location_ids[0:2]:
                 url = "http://api.openweathermap.org/data/2.5/weather?id={}&APPID={}".format(location_id,API_KEY)
                 async with aiohttp.request('GET',url) as weather_request:
                    weather_data  = await weather_request.json()
                    wind_speed = weather_data["wind"]["speed"]
                    wind_speed_knots = self.convert_speed(wind_speed)
                    city_name = weather_data["name"]
                    await self.bot.say("Current wind speed in {}: {} knots.".format(city_name,wind_speed_knots))
         else:
            await self.bot.say("I can't find any information for this location. Please try a different location.")

    def get_location_ids(self,location_name):
        location_name = "_".join(location_name)
        if "_" in location_name:
            location_name = location_name.split("_")
        else:
            location_name = [location_name]
        location_ids = []
        for word in location_name:
            word = word.title()
            location_ids += [location["id"] for location in city_data if word in location["name"].split()]
        
        return location_ids

    def convert_speed(self,speed):
        convertion_factor = 1.943844
        return round(speed*convertion_factor,2)

def setup(bot):
     # Set up background tasks
    bot.add_cog(Weather(bot))
