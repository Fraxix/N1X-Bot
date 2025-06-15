import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from Logger.logger import setup_logger

load_dotenv(dotenv_path="Dev/.env")
TOKEN = os.getenv('TOKEN')
log = setup_logger()

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    log.info(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=" >help | N1X at your service"))

@bot.event
async def on_disconnect():
    log.info("Bot disconnected.")

@bot.event
async def on_resumed():
    log.info("Bot resumed a session.")
    
@bot.event
async def setup_hook():
    await bot.load_extension("Commands.general")
    await bot.load_extension("Commands.moderation")
    await bot.load_extension("Commands.misc")

bot.run(TOKEN)
