import os
import discord
import aiomysql
from discord.ext import commands

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True  # Active la lecture des messages

# Création du bot avec le préfixe "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# Récupération de l'URL MySQL depuis Railway
MYSQL_URL = os.getenv("MYSQL_URL")

async def get_db_connection():
    """Établit une connexion à la base de données MySQL."""
    return await aiomysql.connect(
        host=os.getenv("MYSQLHOST"),
        port=int(os.getenv("MYSQLPORT")),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        db=os.getenv("MYSQLDATABASE"),
        autocommit=True
    )

# Commande qui enregistre le pseudo de l'utilisateur
@bot.command(name="nom")
async def mon_nom(ctx):
    pseudo = ctx.author.name  # Récupère le pseudo Discord

    try:
        # Connexion à la base de données
        conn = await get_db_connection()
        async with conn.cursor() as cursor:
            # Insère le pseudo dans la base de données
            await cursor.execute("INSERT INTO test (texte_test) VALUES (%s)", (pseudo,))
            await conn.commit()

        await ctx.send(f"{pseudo}, ton pseudo a été enregistré en base de données ! 🎉")

    except Exception as e:
        await ctx.send("Une erreur s'est produite lors de l'enregistrement en base de données.")
        print(f"Erreur MySQL: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Récupère le token depuis les variables d'environnement
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise ValueError("Aucun token n'a été trouvé. Configure la variable d'environnement DISCORD_TOKEN.")
    
    # Démarre le bot
    bot.run(TOKEN)
