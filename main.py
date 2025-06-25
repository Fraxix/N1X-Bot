import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from Database.database_connection import get_prefix
from Logger.logger import setup_logger

load_dotenv(dotenv_path="Dev/.env")
TOKEN = os.getenv('TOKEN')
log = setup_logger()

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

@bot.event
async def setup_hook():
    for filename in os.listdir('./Commands'):
        if filename.endswith('.py'):
            category_name = f'Commands.{filename[:-3]}'
            try:
                await bot.load_extension(category_name)
                log.info(f'Successfully loaded extension: {category_name}')
            except Exception as e:
                log.error(f'Failed to load extension: {category_name}: {e}')
bot.run(TOKEN)
