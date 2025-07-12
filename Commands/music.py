import discord
from discord.ext import commands
from Logger.logger import setup_logger

log = setup_logger()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(brief="Makes the bot join your voice channel")
    async def join(self, ctx):
         if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
            try:
                await channel.connect()
                await ctx.send(f"Joined voice channel: {channel.name}")
                log.info(f"{ctx.author} made the bot join voice channel: {channel.name}")
            except discord.ClientException:
                await ctx.send("I'm already connected to a voice channel.")
                log.warning(f"{ctx.author} tried to make the bot join a channel, but it was already connected.")
            except discord.Forbidden:
                await ctx.send("I don't have permission to join that voice channel.")
                log.warning(f"{ctx.author} tried to make the bot join {channel.name}, but lacked permissions.")
            except discord.HTTPException as e:
                await ctx.send("Failed to join the voice channel. Please try again.")
                log.error(f"Error joining voice channel {channel.name} by {ctx.author}. Error: {e}")
         else:
            await ctx.send("You're not connected to a voice channel.")
            log.info(f"{ctx.author} tried to use join but wasn't in a voice channel.")
            
    @commands.command(brief="Makes the bot leave your voice channel")
    async def leave(self, ctx):
         if ctx.voice_client:
             channel_name = ctx.voice_client.channel.name
             await ctx.voice_client.disconnect()
             await ctx.send(f"Disconnected from voice channel: {channel_name}")
             log.info(f"{ctx.author} removed the bot from the voice channel: {channel_name}.")
         else:
             await ctx.send("I'm not connected to any voice channel.")
             log.warning(f"{ctx.author} tried to use leave but the bot wasn't connected to a voice channel.")
            
async def setup(bot):
    await bot.add_cog(Music(bot))