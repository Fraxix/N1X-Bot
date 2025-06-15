import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="Dev/.env")

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Latency: {latency}ms")
        
    @commands.command()
    async def status(self, ctx):
        website_url = os.getenv('DISCORD_WEBHOOK')
        webhook_url = os.getenv('WEBSITE')

        website_status = check_online(website_url)
        webhook_status = check_online(webhook_url)

        embed = discord.Embed(
            title="🔎 Service Status",
            color=discord.Color.green() if website_status and webhook_status else discord.Color.orange()
        )
        embed.add_field(name="🌐 Website", value="✅ Online" if website_status else "❌ Offline", inline=False)
        embed.add_field(name="📡 Webhook", value="✅ Online" if webhook_status else "❌ Offline", inline=False)

        await ctx.send(embed=embed)

def check_online(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code in [200, 204, 301, 302]
    except requests.RequestException:
        return False
        
async def setup(bot):
    await bot.add_cog(General(bot))