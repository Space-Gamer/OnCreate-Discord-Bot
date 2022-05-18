import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_up = bot.botup

    @commands.hybrid_group(name='general')
    async def general(self, ctx):
        """General commands"""
        pass

    @general.command(name='ping', help="To check latency of bot. Also to check if he's alive!")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')


async def setup(bot):
    await bot.add_cog(General(bot))