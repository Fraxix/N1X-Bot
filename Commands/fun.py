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

    @commands.command(help="Reverses the given text.")
    async def reverse(self, ctx, *, text: str = None):
        if not text:
            await ctx.send("Please provide some text to reverse.")
            return

        reversed_text = text[::-1]
        await ctx.send(reversed_text)
        
async def setup(bot):
    await bot.add_cog(Fun(bot))
    