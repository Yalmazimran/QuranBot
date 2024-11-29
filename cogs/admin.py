import discord
from discord.ext import commands
import json

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        """Guides the admin through the bot setup process."""
        await ctx.send("Please provide the loop video link:")
        loop_link = await self.bot.wait_for('message')

        await ctx.send("Please provide the playlist link containing all 114 surahs:")
        playlist_link = await self.bot.wait_for('message')

        await ctx.send("Please mention the voice channel for playback:")
        voice_channel = await self.bot.wait_for('message')

        await ctx.send("Please mention the text channel for public commands:")
        text_channel = await self.bot.wait_for('message')

        # Save to config
        config = {
            "loop_link": loop_link.content,
            "playlist_link": playlist_link.content,
            "voice_channel": voice_channel.content,
            "text_channel": text_channel.content
        }

        with open('./data/config.json', 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send("Setup is complete!")

async def setup(bot):
    await bot.add_cog(Admin(bot))
