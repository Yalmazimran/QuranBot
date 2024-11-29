import discord
from discord.ext import commands
import json

class Playback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def join_channel(self, ctx):
        """Joins the specified voice channel."""
        with open('./data/config.json', 'r') as f:
            config = json.load(f)
        channel = discord.utils.get(ctx.guild.voice_channels, name=config["voice_channel"])
        if channel:
            await channel.connect()

async def setup(bot):
    await bot.add_cog(Playback(bot))
