import discord
from discord.ext import commands
from Logger.logger import setup_logger

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
            deleted = await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"{ctx.author} cleared {amount} messages in channel {ctx.channel}.", delete_after=5)
            log.info(f"{ctx.author} cleared {amount} messages in channel {ctx.channel}.")  
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages.")
            log.warning(f"{ctx.author} tried to clear messages, but the bot lacked permissions.")
        except discord.HTTPException as e:
            await ctx.send("Clear failed. Please try again.")
            log.error(f"Clear Failed. Error {e}")
            
async def setup(bot):
    await bot.add_cog(Moderation(bot))