import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def coinflip(self, ctx):
        result = random.choice(["Heads", "Tails"])
        await ctx.send(f"🪙 The coin landed on: **{result}**!")
        
    @commands.command()
    async def say(self, ctx):
        content = ctx.message.content
        Message = content.replace(">say", "")
        await ctx.send(Message)
        
async def setup(bot):
    await bot.add_cog(Fun(bot))
    