import discord
from discord.ext import commands
import mysql.connector
import os
from dotenv import load_dotenv
from Logger.logger import setup_logger

log = setup_logger()
load_dotenv(dotenv_path="Dev/.env")

def get_db_connection():
    return mysql.connector.connect(
        host= os.getenv('dbHost'),
        user= os.getenv('dbUser'),
        password= os.getenv('dbPassword'),
        database= os.getenv('dbName'),
    )
    
def get_prefix(bot, message):
    if not message.guild:
        return ">"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT prefix FROM Settings WHERE guild_id = %s", (message.guild.id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else ">"
    except Exception as e:
        log.info(f"DB error in get_prefix: {e}")
        return ">"
