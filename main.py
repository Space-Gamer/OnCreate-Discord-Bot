import asyncio
import logging
from datetime import datetime
from os import getenv
from traceback import format_exc

import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, CommandNotFound  # , HybridCommandError
from dotenv import load_dotenv

# from discord.app_commands.commands import AppCommandError

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='\\', intents=intents)

bot.botup = datetime.utcnow()
bot.owner_id = 749892845527367741

# tree = bot.tree

bot.extns = ['cogs.general', 'cogs.fun']


async def load():
    for i in bot.extns:
        await bot.load_extension(i)


@bot.command(name='sync', help='To sync application commands for all guilds.', hidden=True)
# Command to sync application commands for all guilds.
async def sync(ctx):
    if ctx.author.id != bot.owner_id:
        await ctx.send('You are not my owner!')  # Raise PermissionError
        return
    op = await ctx.send('Reloading..')
    for i in bot.extns:
        await bot.reload_extension(i)
    bot.help_command.cog = bot.cogs.get('General')
    await op.edit(content='Reloaded!')
    await op.edit(content='Syncing...')
    await bot.tree.sync()
    await op.edit(content='Reloaded and Synced!')


@bot.command(name='sync_guild', help='To sync application commands for current guild.', hidden=True)
# Command to sync application commands for current guild.
@commands.has_permissions(administrator=True)
async def sync_guild(ctx):
    if ctx.author.id != bot.owner_id:
        await ctx.send('You are not my owner!')  # Raise PermissionError
        return
    op = await ctx.send('Reloading..')
    for i in bot.extns:
        await bot.reload_extension(i)
    bot.help_command.cog = bot.cogs.get('General')
    await op.edit(content='Reloaded!')
    await op.edit(content='Syncing...')
    await bot.tree.sync(guild=ctx.guild)
    await op.edit(content='Reloaded and Synced!')


@bot.command(name='reload', help='To reload all cogs.', hidden=True)  # Command to reload all cogs
@commands.has_permissions(administrator=True)
async def reload(ctx):
    if ctx.author.id != bot.owner_id:
        await ctx.send('You are not my owner!')  # Raise PermissionError
        return
    for i in bot.extns:
        await bot.reload_extension(i)
    bot.help_command.cog = bot.cogs.get('General')
    await ctx.send('Reloaded!')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name='\help', type=discord.ActivityType.listening))
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    await asyncio.sleep(1)
    if isinstance(error, MissingPermissions):
        content = f'You do not have the required permissions to use this command!'
    elif isinstance(error, CommandNotFound):
        content = f'Such a command not found! Use `\\help` to see all commands.'
    else:
        content = f'Something\'s wrong and I can feel it.Command raised an error:\n`{error}`'
        logger.error(format_exc().replace('\n', '\\n'))
    try:
        await ctx.reply(content)  # , ephemeral=True)
    except discord.HTTPException:
        await ctx.reply(content)  # , ephemeral=True)


async def main():
    async with bot:
        await bot.loop.create_task(load())
        bot.help_command.cog = bot.cogs.get('General')
        await bot.start(TOKEN)


asyncio.run(main())
