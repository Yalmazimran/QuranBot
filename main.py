import tracemalloc
tracemalloc.start()

import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Define bot and prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents)

# Load cogs dynamically with error handling
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')  # Await this line
                logging.info(f"Loaded extension: {filename}")
            except Exception as e:
                logging.error(f"Failed to load extension {filename}: {e}")

# This will run once the bot is ready
@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}!")
    await bot.change_presence(activity=discord.Game(name="Quran Recitation"))
    
    # Load extensions once the bot is ready
    await load_extensions()  # Add 'await' here to properly await the coroutine

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))




