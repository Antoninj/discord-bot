import discord
import asyncio
from discord.ext import commands
import aiohttp
from chatterbot import ChatBot

class Chat:
    """Chat related commands
    """
    def __init__(self, bot):
        self.bot = bot
        self.chatbot = ChatBot('Nestor',
                trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
                #storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                 #database='chatterbot-database',
                logic_adapters=[
                {
                   'import_path': "chatterbot.logic.BestMatch"
                },
                {
                'import_path':'chatterbot.logic.MathematicalEvaluation'
                },
                {
                'import_path':'chatterbot.logic.TimeLogicAdapter'
                },
                ],
                #filters=["chatterbot.filters.RepetitiveResponseFilter"],
                #preprocessors=[
                #'chatterbot.preprocessors.clean_whitespace'
                #'chatterbot.preprocessors.convert_to_ascii']
                 )
        self.chatbot.train('chatterbot.corpus.english')

    @commands.command(pass_context=True)
    async def chat(self, ctx):
        """Chat with nestor
        Nestor will have a conversation with you.
        eg. *hello Nestor"""
        await self.bot.say("Hi, how are you?")
        while True:
            answer = await self.bot.wait_for_message(author=ctx.message.author, timeout = 10.0)
            if answer is None:
                fmt = 'Sorry, you took too long to answer, good bye.'
                await self.bot.say(fmt)
                break
                return
            
            else:
                response = self.chatbot.get_response(answer.content)
                await self.bot.say(response)

def setup(bot):
    bot.add_cog(Chat(bot))