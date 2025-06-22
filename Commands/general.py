import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os
import psutil
import time

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
        start_time = time.perf_counter()
        website_url = os.getenv('WEBSITE')
        webhook_url = os.getenv('DISCORD_WEBHOOK')
        
        cpu_usage = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        ram_usage = memory.percent
        bot_latency = self.bot.latency * 1000

        website_status = check_online(website_url)
        webhook_status = check_online(webhook_url)
        
        elapsed = (time.perf_counter() - start_time) * 1000 

        embed = discord.Embed(
            title="🔎 Service Status",
            color=discord.Color.green() if website_status and webhook_status else discord.Color.orange()
        )
        embed.add_field(name="🌐 Website", value="✅ Online" if website_status else "❌ Offline", inline=False)
        embed.add_field(name="📡 Webhook", value="✅ Online" if webhook_status else "❌ Offline", inline=False)
        embed.add_field(
            name="🤖 N1X Bot",
            value=(
                f"📶 Ping: `{bot_latency:.2f} ms`\n"
                f"🧠 RAM: `{ram_usage:.1f}%`\n"
                f"🖥️ CPU: `{cpu_usage:.1f}%`\n"
                f"⚙️ Status Check Time: `{elapsed:.2f} ms`"
            ),
            inline=False
        )

        await ctx.send(embed=embed)
        
    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        roles = [role.mention for role in member.roles[1:]]
        roles_display = ", ".join(roles[:5]) + ("..." if len(roles) > 5 else "") or "No roles"

        embed = discord.Embed(
            title=f"User Info: {member}",
            color=member.color,
            timestamp=ctx.message.created_at
        )

        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Display Name", value=member.display_name, inline=True)
        embed.add_field(name="Status", value=str(member.status).title(), inline=True)
        embed.add_field(name="Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name=f"Roles ({len(member.roles)-1})", value=roles_display, inline=False)
    
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        await ctx.send(embed=embed)
        
    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild

        embed = discord.Embed(
            title=f"Server Info - {guild.name}",
            color=discord.Color.blue(),
            timestamp=ctx.message.created_at
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        if guild.banner:
            embed.set_image(url=guild.banner.url)

        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Region", value=str(guild.preferred_locale).capitalize(), inline=True)
        embed.add_field(name="Verification Level", value=str(guild.verification_level).capitalize(), inline=True)
        embed.add_field(name="Boost Level", value=str(guild.premium_tier), inline=True)
        embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Created On", value=guild.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

        await ctx.send(embed=embed)


def check_online(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code in [200, 204, 301, 302]
    except requests.RequestException:
        return False
        
async def setup(bot):
    await bot.add_cog(General(bot))