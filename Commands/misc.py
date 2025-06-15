import discord
from discord.ext import commands
import requests

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def dog(self,ctx):
        url = "https://dog.ceo/api/breeds/image/random"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data["status"] == "success":
                embed = discord.Embed(title="🐶 Random Doggo")
                embed.set_image(url=data["message"])
                await ctx.send(embed=embed)
            else:
                await ctx.send("Failed to get a dog image!")

        except requests.RequestException:
            await ctx.send("Error fetching dog image. Try again later.")
            
    @commands.command()
    async def shiba(self,ctx):
        url = "https://dog.ceo/api/breed/shiba/images/random"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data["status"] == "success":
                embed = discord.Embed(title="🐕 Shiba Inu")
                embed.set_image(url=data["message"])
                await ctx.send(embed=embed)
            else:
                await ctx.send("Failed to get a dog image!")

        except requests.RequestException:
            await ctx.send("Error fetching dog image. Try again later.")
           
        
        
async def setup(bot):
    await bot.add_cog(Misc(bot))