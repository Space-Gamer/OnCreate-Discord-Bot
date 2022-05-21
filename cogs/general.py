import datetime as dt
from datetime import datetime

import discord
from discord.ext import commands


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
        await ctx.reply(f'Pong! `{round(self.bot.latency * 1000)} ms`')

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

    @commands.hybrid_command(name='guilds', description='Display the guild names the bot is in.', hidden=True)
    async def guilds(self, ctx):
        guilddict = {guild.name: guild.member_count for guild in self.bot.guilds}
        strr, i = '', 1
        for key, value in sorted(guilddict.items(), key=lambda item: item[1], reverse=True):
            strr += f"{i}. {key} - `{value} members`\n"
            i += 1
        await ctx.send(embed=discord.Embed(title='Guilds',
                                           description=strr,
                                           colour=discord.Colour.random()))

    @commands.hybrid_command(name='suggest', description='Suggests a feature for the bot.',
                             help='Suggests a bot feature.')
    @discord.app_commands.describe(suggestion='The feature you want to suggest.')
    async def suggest(self, ctx, suggestion: str):
        embedd = discord.Embed(title='Suggestion', description=f"{suggestion}", colour=discord.Colour.random(),
                               timestamp=datetime.utcnow() + dt.timedelta(hours=5, minutes=30)) \
            .set_thumbnail(url=ctx.message.author.avatar).set_footer(text=f"Suggested by {ctx.author.name}")
        await self.bot.get_guild(934632146948227133).get_channel(934632149477359646). \
            send(embed=embedd)
        await ctx.reply(embed=embedd)
        await ctx.reply('Thank you for your suggestion!',
                        delete_after=5)

    @commands.hybrid_command(name='about', description='Gives information about the bot.',
                             help='Gives info about the bot.')
    async def about(self, ctx):
        await ctx.send("**About OnCreate 2.O:**"
                       "\n\n+ Uses `discord.py 2.0(Beta)`"
                       "\n+ **Created by:** `Space Gamer`"
                       "\n+ **Repository link:** https://github.com/Space-Gamer/OnCreate-Discord-Bot"
                       "\n+ **Invite link:** https://discord.com/api/oauth2/authorize?client_id=976516646392963164"
                       "&permissions=311623411777&scope=bot%20applications.commands")


async def setup(bot):
    await bot.add_cog(General(bot))
