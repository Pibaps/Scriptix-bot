import os
import discord
import aiomysql
from discord.ext import commands

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True  # Active la lecture des messages

# Création du bot avec le préfixe "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# Récupération des variables MySQL
MYSQL_HOST = os.getenv("MYSQLHOST")
MYSQL_PORT = os.getenv("MYSQLPORT")
MYSQL_USER = os.getenv("MYSQLUSER")
MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQLDATABASE")

if not all([MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE]):
    raise ValueError("Une ou plusieurs variables d'environnement MySQL sont manquantes.")

async def get_db_connection():
    """Établit une connexion à la base de données MySQL."""
    try:
        return await aiomysql.connect(
            host=MYSQL_HOST,
            port=int(MYSQL_PORT),  # Assure que la conversion en int fonctionne
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DATABASE,
            autocommit=True
        )
    except Exception as e:
        print(f"Erreur de connexion à MySQL : {e}")
        return None  # Retourne None en cas d'erreur

# Commande qui enregistre le pseudo de l'utilisateur
@bot.command(name="nom")
async def mon_nom(ctx):
    pseudo = ctx.author.name  # Récupère le pseudo Discord
    conn = None  # Initialise la connexion pour éviter l'UnboundLocalError

    try:
        # Connexion à la base de données
        conn = await get_db_connection()
        if conn is None:
            await ctx.send("Erreur : Impossible de se connecter à la base de données.")
            return

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
