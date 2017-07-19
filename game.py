import discord
from discord.ext import commands
import asyncio

import aiohttp
from lxml import html

import random
from random import randint


class Game:
    """Game related commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def curve(self, *name : str):
        """Curve fever rank information
        Nestor will tell you your curve fever ffa and team ranks.
        eg. *rank antonin"""

        url = 'http://forum.curvefever.com/users/{}'.format("-".join(name))

        async with aiohttp.request('GET',url) as cf_website:
            data  = await cf_website.text()
            tree = html.fromstring(data)
            player_ranks= tree.xpath('//div[@class="profile"][1]/dl/dd/text()')
            player_ranks_info= tree.xpath('//div[@class="profile"][1]/dl/dt/text()')

            player_ranks_info = [str(item) +":" for item in player_ranks_info]
            player_info = list(zip(player_ranks_info,player_ranks))

            player_info  = [" ".join(item) for item in player_info]
            player_info = '\n'.join(player_info[:len(player_info)-1])

            await self.bot.say(player_info)


    @commands.command(pass_context=True)
    async def guess(self, ctx):
        """Guess a number game
        Nestor will play the guessing game.
        eg. *guess"""

        def guess_check(m):
                return m.content.isdigit()

        await self.bot.say('Lets play a game! You have to guess a number '
                                'between 1 and 10.')
        guess = await self.bot.wait_for_message(author=ctx.message.author, check = guess_check, timeout = 5.0)

        answer = random.randint(1, 10)
        counter = 0

        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await self.bot.say(fmt.format(answer))
            return

        while counter<=3:
            counter += 1
            if counter<3:
                if int(guess.content) > answer:
                    await self.bot.say('Your guess is too high! Try again.')
                    guess = await self.bot.wait_for_message(author=ctx.message.author)

                elif int(guess.content) < answer:
                    await self.bot.say('Your guess is too low! Try again.')
                    guess = await self.bot.wait_for_message(author=ctx.message.author)

                elif counter == 1 and int(guess.content) == answer:
                        await self.bot.say('Cogratulations! You got it on your first try!')
                        break

                elif int(guess.content) == answer and counter !=1 :
                    await self.bot.say('Congratulations! It took you '
                    '**%d** tries to guess the correct answer.' % counter)
                    break

            elif counter ==3 and int(guess.content) == answer :
                await self.bot.say('Congratulations! It took you '
                    '**%d** tries to guess the correct answer.' % counter)
                break

            else:
                await self.bot.say('Sorry, It was {}.'.format(answer))
                break


    @commands.command(pass_context=True)
    async def rps(self, ctx):
        """Rock, Paper, Scissors game 
        Nestor will play Rock, Paper, Scissors.
        eg. *rps"""

        while True:
            await self.bot.say('Lets play **Rock, Paper, Scissors**. '
            'Pick your weapon (rock, paper or scissors) :')
            choices = ['rock', 'paper', 'scissors']
            computer_choice = choices[randint(0, 2)]
            player_response = await self.bot.wait_for_message(author=ctx.message.author)
            player_choice = player_response.content

            beats = {
                'rock': ['paper'],
                'paper': ['scissors'],
                'scissors': ['rock']
            }

            while computer_choice and player_choice in choices:
                if computer_choice == player_choice:
                    result = '**Tie!** You both chose **%s**. ' % player_choice
                    await self.bot.say(result)
                    break
                elif player_choice in beats[computer_choice]:
                    result = '**You win!** Nestor chose: **%s** ' % computer_choice + 'and you chose: **%s**. ' % player_choice
                    await self.bot.say(result)
                    break
                else:
                    result = '**You lose!** Nestor chose: **%s** ' % computer_choice + 'and you chose: **%s**. ' % player_choice
                    await self.bot.say(result)
                    break
            while computer_choice and player_choice in choices:
                await self.bot.say('Do you want to play again? '
                '(Enter: **Yes** / **No**)')
                repeat_response = await self.bot.wait_for_message(author=ctx.message.author)
                repeat_choice = repeat_response.content

                if repeat_choice.lower() == 'yes':
                    break
                elif repeat_choice.lower() == 'no':
                    await self.bot.say('Thanks for playing!')
                    return False
                else:
                    await self.bot.say('Invalid option!')
                continue
            else:
                await self.bot.say('Invalid option')
                continue

def setup(bot):
    bot.add_cog(Game(bot))
