import asyncio
import discord
from discord.ext import commands
from Logger.logger import setup_logger
from Database.database_connection import get_db_connection

log = setup_logger()

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
          
    @commands.command(brief="Bans a user from the Server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"✅ {member.mention} has been banned. Reason: {reason if reason else 'No reason provided.'}")
            log.info(f"{ctx.author} banned {member} | Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to ban that user.")
            log.warning(f"{ctx.author} tried to ban {member} but lacked permissions.")
        except discord.HTTPException as e:
            await ctx.send("Ban failed. Please try again.")
            log.error(f"Failed to ban {member} by {ctx.author}. Error: {e}")
            
    @commands.command(brief="Kicks a user from the Server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f"✅ {member.mention} has been kicked. Reason: {reason if reason else 'No reason provided.'}")
            log.info(f"{ctx.author} kicked {member} | Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to kick that user.")
            log.warning(f"{ctx.author} tried to kick {member} but lacked permissions.")
        except discord.HTTPException as e:
            await ctx.send("Kick failed. Please try again.")
            log.error(f"Failed to kick {member} by {ctx.author}. Error: {e}")
        
    @commands.command(brief="Clears a user selected amount of Messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx, amount: int):
        try:
            if amount < 1:
                await ctx.send("Please select atleast 1 message")
                return 
            deleted_messages = await ctx.channel.purge(limit=amount + 1)
            deleted_count = len(deleted_messages) - 1
            await ctx.send(f"{ctx.author} cleared {deleted_count} messages in channel {ctx.channel}.", delete_after=5)
            log.info(f"{ctx.author} cleared {deleted_count} messages in channel {ctx.channel}. Wanted to delete {deleted_messages -1}")  
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages.")
            log.warning(f"{ctx.author} tried to clear messages, but the bot lacked permissions.")
        except discord.HTTPException as e:
            await ctx.send("Clear failed. Please try again.")
            log.error(f"Clear Failed. Error {e}")
            
    @commands.command(brief="Nuke all messages in a Channel")
    @commands.has_permissions(manage_channels=True)
    async def nuke(self,ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in ["yes", "no"]
        await ctx.send(f"{ctx.author.mention}, are you sure you want to nuke this channel? Reply with `yes` or `no`.")
        
        try:
            confirmation = await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("⏰ Nuke command timed out. Cancelled.")
            return
        
        if confirmation.content.lower() == "yes":
            channel = ctx.channel
            new_channel = await channel.clone()
            await channel.delete()
            await new_channel.send("💥 This channel was nuked!")
        else:
            await ctx.send("❌ Nuke command cancelled.")

    @commands.command(name="setprefix", brief="Set a custom prefix for this server")
    @commands.has_guild_permissions(administrator=True)
    async def setprefix(self, ctx, new_prefix: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                REPLACE INTO prefixes (guild_id, prefix, guild_name)
                VALUES (%s, %s, %s)
                """,
                (ctx.guild.id, new_prefix, ctx.guild.name)
            )
            conn.commit()
            cursor.close()
            conn.close()
            await ctx.send(f"Prefix updated to `{new_prefix}` for guild `{ctx.guild.name}`")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))