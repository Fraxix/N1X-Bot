import discord
from discord.ext import commands
from Database.database_connection import get_db_connection
from Logger.logger import setup_logger

log = setup_logger()

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(f'Logged in as {self.bot.user.name}')
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=" >help | N1X at your service"))
        for guild in self.bot.guilds:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO guild_settings (guild_id, guild_name, owner_id, prefix)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        guild_name = VALUES(guild_name),
                        owner_id = VALUES(owner_id)
                    """,
                    (guild.id, guild.name, guild.owner_id if guild.owner else None, ">")
                )
                conn.commit()
                cursor.close()
                conn.close()
                log.info(f"Synced guild on startup: {guild.name} ({guild.id})")
                
            except Exception as e:
                log.error(f"Error syncing guild {guild.name} ({guild.id}): {e}")
        log.info("All guilds synced successfully on startup.")
        
    @commands.Cog.listener()
    async def on_disconnect(self):
        log.info("Bot disconnected.")

    @commands.Cog.listener()
    async def on_resumed(self):
        log.info("Bot resumed a session.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="general")
        if channel:
            await channel.send(f"{member.mention} has joined the server!")
            log.info(f"{member} has joined the server!")
        else:
            log.error("No general channel found!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="general")
        if channel:
            await channel.send(f"{member.mention} has left the server!")
            log.info(f"{member} has left the server!")
        else:
            log.error("No general channel found!")
            
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO guild_settings (guild_id, guild_name, owner_id, prefix)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    guild_name = VALUES(guild_name),
                    owner_id = VALUES(owner_id)
                """,
                (
                    guild.id,
                    guild.name,
                    guild.owner_id if guild.owner else None,
                    ">"
                )
            )
            conn.commit()
            cursor.close()
            conn.close()
            log.info(f"Joined new guild: {guild.name} ({guild.id}) | Owner: {guild.owner} ({guild.owner_id})")
        except Exception as e:
            log.error(f"Failed to save guild info for {guild.name} ({guild.id}): {e}")

async def setup(bot):
    await bot.add_cog(Events(bot))
