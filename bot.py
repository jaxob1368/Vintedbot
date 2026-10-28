from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

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

# Uruchomienie bota
TOKEN = os.getenv("DISCORD_TOKEN")
if __name__ == "__main__":
    bot.run(TOKEN)
