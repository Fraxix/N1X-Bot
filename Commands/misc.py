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
            
    @commands.command()
    async def samoyed(self,ctx):
        url = "https://dog.ceo/api/breed/samoyed/images/random"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data["status"] == "success":
                embed = discord.Embed(title="🐕❄️ Samoyed")
                embed.set_image(url=data["message"])
                await ctx.send(embed=embed)
            else:
                await ctx.send("Failed to get a dog image!")

        except requests.RequestException:
            await ctx.send("Error fetching dog image. Try again later.")
    
    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        embed = discord.Embed(
            title=f"{member.display_name}'s Avatar",
            color=discord.Color.blurple()
        )
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

        
        
async def setup(bot):
    await bot.add_cog(Misc(bot))