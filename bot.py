import os
import discord
from discord.ext import commands

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True  # Active la lecture des messages

# Création du bot avec le préfixe "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# Commande qui affiche le nom du bot
@bot.command(name="nom")
async def mon_nom(ctx):
    await ctx.send(f"Je suis {bot.user.name} !")  # Affiche le vrai nom du bot

if __name__ == "__main__":
    # Récupère le token depuis les variables d'environnement
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if not TOKEN:
        raise ValueError("Aucun token n'a été trouvé. Configure la variable d'environnement DISCORD_TOKEN.")
    
    # Démarre le bot
    bot.run(TOKEN)
