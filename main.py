import discord
import asyncio
import logging
from traceback import format_exc
from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from discord.ext import commands
from discord.app_commands import AppCommandError, MissingPermissions

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
# intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='\\', intents=intents)

bot.botup = datetime.utcnow()
bot.owner_id = 749892845527367741

tree = bot.tree

bot.extns = ['cogs.general']


async def load():
    for i in bot.extns:
        await bot.load_extension(i)


@bot.command(name='sync', help='To sync application commands for all guilds.')
@commands.has_permissions(administrator=True)
async def sync(ctx):
    if ctx.author.id != bot.owner_id:
        await ctx.send('You are not my owner!')  # Raise PermissionError
        return
    op = await ctx.send('Reloading..')
    for i in bot.extns:
        await bot.reload_extension(i)
    await op.edit(content='Reloaded!')
    await op.edit(content='Syncing...')
    await bot.tree.sync()
    await op.edit(content='Reloaded and Synced!')


@bot.command(name='sync_guild', help='To sync application commands for current guild.')
@commands.has_permissions(administrator=True)
async def sync_guild(ctx):
    if ctx.author.id != bot.owner_id:
        await ctx.send('You are not my owner!')  # Raise PermissionError
        return
    op = await ctx.send('Reloading..')
    for i in bot.extns:
        await bot.reload_extension(i)
    await op.edit(content='Reloaded!')
    await op.edit(content='Syncing...')
    await bot.tree.sync(guild=ctx.guild)
    await op.edit(content='Reloaded and Synced!')


@bot.command(name='reload', help='To reload all cogs.')
@commands.has_permissions(administrator=True)
async def reload(ctx):
    if ctx.author.id != bot.owner_id:
        await ctx.send('You are not my owner!')  # Raise PermissionError
        return
    for i in bot.extns:
        await bot.reload_extension(i)
    await ctx.send('Reloaded!')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name='\help', type=discord.ActivityType.listening))
    print(f'{bot.user.name} has connected to Discord!')


@tree.error
async def app_command_error(interaction: discord.Interaction, error: AppCommandError):
    await asyncio.sleep(1)
    if isinstance(error, MissingPermissions):
        content = f'You do not have the required permissions to use this command!'
    else:
        content = f'Something\'s wrong and I can feel it.Command raised an error:\n`{error}`'
        logger.error(format_exc().replace('\n', '\\n'))
    try:
        await interaction.response.send_message(content, ephemeral=True)
    except discord.HTTPException:
        await interaction.followup.send(content, ephemeral=True)


async def main():
    async with bot:
        bot.loop.create_task(load())
        await bot.start(TOKEN)

asyncio.run(main())
