import os
import discord
from discord.ext import commands
from vinted_scraper import VintedScraper

# Konfiguracja bota
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Inicjalizacja scrapera Vinted (automatycznie radzi sobie z sesjami)
vinted = VintedScraper("https://www.vinted.pl")

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}!")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong! Bot Vinted działa w chmurze 24/7.")

@bot.command(name="vinted")
async def vinted_search(ctx, *, query: str = "nike"):
    """Przeszukuje Vinted za pomocą dedykowanej biblioteki"""
    await ctx.send(f"🔍 Szukam na Vinted frazy: **{query}**...")
    
    try:
        # Wyszukiwanie przedmiotów przez oficjalny moduł
        items = vinted.items.search(query, {"per_page": 3})
        
        if not items:
            await ctx.send("❌ Nie znaleziono żadnych przedmiotów dla tej frazy.")
            return
        
        for item in items[:3]:
            # Obsługa różnych formatów zwracanych danych przez bibliotekę
            title = getattr(item, "title", None) or item.get("title")
            price = getattr(item, "price", None) or item.get("price")
            currency = getattr(item, "currency", None) or item.get("currency", "PLN")
            item_url = getattr(item, "url", None) or item.get("url")
            
            # Pobieranie zdjęcia
            photo = getattr(item, "photo", None) or item.get("photo")
            photo_url = None
            if isinstance(photo, dict):
                photo_url = photo.get("url")
            elif hasattr(photo, "url"):
                photo_url = photo.url
                
            message = f"**{title}**\n💰 Cena: **{price} {currency}**\n🔗 [Zobacz ogłoszenie]({item_url})"
            if photo_url:
                message += f"\n{photo_url}"
                
            await ctx.send(message)
            
    except Exception as e:
        await ctx.send(f"❌ Wystąpił błąd podczas pobierania ofert: {e}")

# Uruchomienie bota
TOKEN = os.getenv("DISCORD_TOKEN")
if __name__ == "__main__":
    bot.run(TOKEN)
