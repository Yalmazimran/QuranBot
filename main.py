import discord
from discord.ext import commands
import os

# Define bot and prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents)

# Load cogs dynamically
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    await bot.change_presence(activity=discord.Game(name="Quran Recitation"))

# Load all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Run the bot
bot.run('YOUR_BOT_TOKEN')
