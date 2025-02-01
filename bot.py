import os
import discord
from discord.ext import commands

# Configuration des intents (tu peux ajuster selon tes besoins)
intents = discord.Intents.default()

# Création du bot avec le préfixe "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# Commande qui affiche le nom du bot
@bot.command(name="nom")
async def mon_nom(ctx):
    # Remplace "MonBot" par le nom souhaité
    await ctx.send("Je suis MonBot !")

if __name__ == "__main__":
    # Récupère le token depuis les variables d'environnement
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if not TOKEN:
        raise ValueError("Aucun token n'a été trouvé. Configure la variable d'environnement DISCORD_TOKEN.")
    
    # Démarre le bot
    bot.run(TOKEN)
