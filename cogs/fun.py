import datetime as dt
import json
import random
from datetime import datetime

import discord
import requests
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='quote', description="Displays inspirational quotes.",
                             help="Gives an inspirational quote.")
    async def quote(self, ctx):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)[0]
        await ctx.reply(embed=discord.Embed(title='Inspirational Quote', colour=discord.Colour.random(),
                                            description="❝ " + str(json_data['q']) + " ❞",
                                            url="https://zenquotes.io/").set_footer(text='- ' + json_data['a']))

    @commands.hybrid_command(name='memes', description='Get memes and display as an embed.',
                             help='Gives random memes.')
    async def memes(self, ctx):
        content = requests.get("https://meme-api.herokuapp.com/gimme").text
        data = json.loads(content, )
        await ctx.reply(embed=discord.Embed(title=data['title'], url=data['postLink'],
                                            colour=discord.Colour.random()).set_image(url=data['url']))

    @commands.hybrid_command(name='dog', description='Gives random images of dogs in embeds.',
                             help='Gives random dog picture.')
    async def dog(self, ctx):
        content = requests.get("https://dog.ceo/api/breeds/image/random").text
        data = json.loads(content, )
        await ctx.reply(embed=discord.Embed(title='Random Dog', url=data['message'],
                                            colour=discord.Colour.random()).set_image(url=data['message']))

    @commands.hybrid_command(name='cat', description='Rarely gives random images of cats in embeds. '
                                                     '\nKeep trying, you might end up getting a cat picture.',
                             help='Gives random cat picture.')
    async def cat(self, ctx):
        if random.choices([True, False], [0.01, 0.99])[0]:
            content = requests.get("https://aws.random.cat/meow").text
            try:
                data = json.loads(content, )
                await ctx.reply(embed=discord.Embed(title='Random Cat', url=data['file'],
                                                    colour=discord.Colour.random()).set_image(url=data['file']))
            except json.decoder.JSONDecodeError:
                await ctx.reply('Bad luck :slight-frown:! Try again.')
        else:
            await ctx.reply('You did not have luck this time. Try again!')

    @commands.hybrid_command(name='dogfact', description='Gives random dog facts.', help='Gives random dog fact.')
    async def dogfact(self, ctx):
        content = requests.get("https://dog-api.kinduff.com/api/facts").text
        data = json.loads(content, )
        if data['success']:
            await ctx.reply(embed=discord.Embed(title='Random Dog Fact', description=data["facts"][0],
                                                colour=discord.Colour.random()))
        else:
            await ctx.reply('Something went wrong. Try again!')

    @commands.hybrid_command(name='iss', help='Gives the current location of the ISS.',
                             description='Gives current location (coordinates) of the International Space Station '
                                         '(ISS).')
    async def iss(self, ctx):
        content = requests.get("http://api.open-notify.org/iss-now.json").text
        data = json.loads(content, )
        await ctx.reply(embed=discord.Embed(title='ISS Location',
                                            description=f'Latitude: `{data["iss_position"]["latitude"]}`'
                                                        f'\nLongitude: `{data["iss_position"]["longitude"]}`',
                                            colour=discord.Colour.random(),
                                            timestamp=datetime.utcnow() + dt.timedelta(hours=5, minutes=30)))

    @commands.hybrid_command(name='bitcoin', description='Gives the current price of Bitcoin.',
                             help='Gives current price of bitcoin.')
    async def bitcoin(self, ctx):
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        data = json.loads(response.text)
        await ctx.reply(embed=discord.Embed(title='Current Bitcoin Price', url='https://www.coindesk.com/price/',
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
        await ctx.reply(embed=discord.Embed(title='Public IP Address', description=f"Your public IP is `{data['ip']}`",
                                            colour=discord.Colour.random()))


async def setup(bot):
    await bot.add_cog(Fun(bot))
