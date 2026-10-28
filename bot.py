import os
import discord
from discord.ext import commands

# Konfiguracja bota
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}!")
    # Tutaj możesz dodać swoją pętlę sprawdzającą Vinted

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong! Bot Vinted działa w chmurze 24/7 bez problemów z Cloudflare.")

# Uruchomienie bota
TOKEN = "MTU2NTA0OTA3MjEzNjYxODAyNA.G_xsyR.8D3a3cx6tfLPj2B22vj8byl7J7R6rsvMbp2iK4"

if __name__ == "__main__":
    bot.run(TOKEN)