import discord
from discord.ext import commands
from Logger.logger import setup_logger

log = setup_logger()

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(f'Logged in as {self.bot.user.name}')
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=" >help | N1X at your service"))

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

async def setup(bot):
    await bot.add_cog(Events(bot))
