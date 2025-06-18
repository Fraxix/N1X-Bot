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
        message = ctx.message.content
        command_text = ctx.prefix + ctx.invoked_with
        args = message[len(command_text):].strip()

        if not args:
            await ctx.send("You didn't tell me what to say!")
        else:
            await ctx.send(args)
        
async def setup(bot):
    await bot.add_cog(Fun(bot))
    