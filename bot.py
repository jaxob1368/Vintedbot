import os
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import discord
from discord.ext import commands

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

# Uruchamiamy serwer w tle, zeby Render widzial otwarty port 10000
threading.Thread(target=run_server, daemon=True).start()

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

@bot.command(name="vinted")
async def vinted_search(ctx, *, query: str = "nike"):
    """Przeszukuje Vinted przez alternatywne API"""
    await ctx.send(f"🔍 Szukam na Vinted frazy: **{query}**...")
    
    url = f"https://www.vinted.pl/api/v2/catalog/items?search_text={query}&per_page=3"
    
    # Używamy stabilniejszego proxy corsproxy.io
    proxy_url = f"https://corsproxy.io/?{requests.utils.quote(url)}"
    
    try:
        response = requests.get(proxy_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            if not items:
                await ctx.send("❌ Nie znaleziono żadnych przedmiotów dla tej frazy.")
                return
            
            for item in items[:3]:
                title = item.get("title")
                price = item.get("price")
                currency = item.get("currency")
                item_id = item.get("id")
                item_url = f"https://www.vinted.pl/items/{item_id}"
                
                photo = item.get("photo", {})
                photo_url = photo.get("photo_url") or (photo.get("url") if photo else None)
                
                message = f"**{title}**\n💰 Cena: **{price} {currency}**\n🔗 [Zobacz ogłoszenie]({item_url})"
                if photo_url:
                    message += f"\n{photo_url}"
                
                await ctx.send(message)
        else:
            await ctx.send(f"⚠️ Proxy zwróciło kod błędu: {response.status_code}")
    except Exception as e:
        await ctx.send(f"❌ Wystąpił błąd: {e}")

# Uruchomienie bota
TOKEN = os.getenv("DISCORD_TOKEN")
if __name__ == "__main__":
    bot.run(TOKEN)
