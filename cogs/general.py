import discord
from discord.ext import commands

from datetime import datetime
import datetime as dt
import requests
import json
import random

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_up = bot.botup

    # @commands.hybrid_group(name='general')
    # async def general(self, ctx):
    #     """General commands"""
    #     pass

    # @general.command(name='ping', description="To check latency of bot. Also to check if he's alive!")
    @commands.hybrid_command('ping', description="To check latency of bot. Also to check if he's alive!",
                             help="To check latency of bot.")
    async def ping(self, ctx):
        await ctx.send(f'Pong! `{round(self.bot.latency * 1000)} ms`')

    @commands.hybrid_command('uptime', description="To check how long bot has been up for.", help="Gives bot uptime.")
    async def uptime(self, ctx):
        diff = datetime.utcnow() - self.bot_up
        days = diff.days
        if days:
            embedd = discord.Embed \
                (title='Uptime',
                 description=f'Up for {days} days {diff.seconds // 3600} hours {(diff.seconds % 3600) // 60} minutes '
                             f'{diff.seconds % 60}  seconds',
                 color=0xff9200)
        else:
            embedd = discord.Embed \
                (title='Uptime',
                 description=f'Up for {diff.seconds // 3600} hours {(diff.seconds % 3600) // 60}'
                             f' minutes {diff.seconds % 60}  seconds',
                 color=0xff9200)
        embedd.set_footer(text='Since {} UTC'.format(self.bot_up.strftime('%a %d-%m-%y %I:%M%p')))
        embedd.timestamp = datetime.now()
        await ctx.send(embed=embedd)
        return

    @commands.hybrid_command(name='hello', description="To greet the bot and get greeted back.",
                             help="Gives bot a greeting.")
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.mention}, Hope you are keeping well!')

    @commands.hybrid_command(name='quote', description="Displays inspirational quotes.",
                             help="Gives an inspirational quote.")
    async def quote(self, ctx):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)[0]
        await ctx.send(embed=discord.Embed(title='Inspirational Quote', colour=discord.Colour.random(),
                                           description="❝ "+str(json_data['q'])+" ❞",
                                           url="https://zenquotes.io/").set_footer(text='- '+json_data['a']))

    @commands.hybrid_command(name='memes', description='Get memes and display as an embed.', help='Gives random memes.')
    async def memes(self, ctx):
        content = requests.get("https://meme-api.herokuapp.com/gimme").text
        data = json.loads(content, )
        await ctx.send(embed=discord.Embed(title=data['title'], url=data['postLink'],
                                           colour=discord.Colour.random()).set_image(url=data['url']))

    @commands.hybrid_command(name='dog', description='Gives random images of dogs in embeds.',
                             help='Gives random dog picture.')
    async def dog(self, ctx):
        content = requests.get("https://dog.ceo/api/breeds/image/random").text
        data = json.loads(content, )
        await ctx.send(embed=discord.Embed(title='Random Dog', url=data['message'],
                                           colour=discord.Colour.random()).set_image(url=data['message']))

    @commands.hybrid_command(name='cat', description='Rarely gives random images of cats in embeds. '
                                                     '\nKeep trying, you might end up getting a cat picture.',
                             help='Gives random cat picture.')
    async def cat(self, ctx):
        if random.choices([True, False], [0.00001, 0.99999])[0]:
            content = requests.get("https://aws.random.cat/meow").text
            data = json.loads(content, )
            await ctx.send(embed=discord.Embed(title='Random Cat', url=data['file'],
                                               colour=discord.Colour.random()).set_image(url=data['file']))
        else:
            await ctx.send('You did not have luck this time. Try again!')

    @commands.hybrid_command(name='dogfact', description='Gives random dog facts.', help='Gives random dog fact.')
    async def dogfact(self, ctx):
        content = requests.get("https://dog-api.kinduff.com/api/facts").text
        data = json.loads(content, )
        if data['success']:
            await ctx.send(embed=discord.Embed(title='Random Dog Fact', description=data["facts"][0],
                                               colour=discord.Colour.random()))
        else:
            await ctx.send('Something went wrong. Try again!')

    @commands.hybrid_command(name='iss', description='Gives the current location of the ISS.',
                             help='Gives current location (coordinates) of the International Space Station (ISS).')
    async def iss(self, ctx):
        content = requests.get("http://api.open-notify.org/iss-now.json").text
        data = json.loads(content, )
        await ctx.send(embed=discord.Embed(title='ISS Location',
                                           description=f'Latitude: `{data["iss_position"]["latitude"]}`'
                                                       f'\nLongitude: `{data["iss_position"]["longitude"]}`',
                                           colour=discord.Colour.random(),
                                           timestamp=datetime.utcnow()+dt.timedelta(hours=5, minutes=30)))

    @commands.hybrid_command(name='bitcoin', description='Gives the current price of Bitcoin.',
                             help='Gives current price of bitcoin.')
    async def bitcoin(self, ctx):
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        data = json.loads(response.text)
        await ctx.send(embed=discord.Embed(title='Current Bitcoin Price', url='https://www.coindesk.com/price/',
                                           description=f"1 BTC = `{data['bpi']['USD']['rate']} USD`",
                                           colour=discord.Colour.random()).
                       set_footer(text=f"Last Updated: {data['time']['updated']}"))

    @commands.hybrid_command(name='bored', description='Suggests ideas or tasks to perform when you\'re bored.',
                             help='Gives you an idea when bored.')
    async def bored(self, ctx):
        response = requests.get("https://www.boredapi.com/api/activity")
        data = json.loads(response.text)
        await ctx.reply(f"I'd suggest a *{data['type']} activity* for you!\nActivity: **{data['activity']}**")

    @commands.hybrid_command(name='ip', description='Displays your public IP Address', help='Gives your public IP.')
    async def ip(self, ctx):
        response = requests.get("https://api.ipify.org?format=json")
        data = json.loads(response.text)
        await ctx.send(embed=discord.Embed(title='Public IP Address', description=f"Your public IP is `{data['ip']}`",
                                           colour=discord.Colour.random()))



async def setup(bot):
    await bot.add_cog(General(bot))