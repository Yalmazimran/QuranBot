import discord
from discord.ext import commands
import json

class Public(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('./data/surah_links.json', 'r') as f:
            self.surah_links = json.load(f)

    @commands.command()
    async def list(self, ctx):
        """Displays all surah names with numbers."""
        surah_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(self.surah_links.keys())])
        message = await ctx.send(f"**Surah List:**\n{surah_list}")
        await message.delete(delay=120)  # Deletes after 2 minutes

    @commands.command()
    async def play(self, ctx, surah_number: int):
        """Plays the specified surah by its number."""
        try:
            surah_name = list(self.surah_links.keys())[surah_number - 1]
            surah_link = self.surah_links[surah_name]

            # Stop the loop and play the surah
            await ctx.send(f"Playing Surah {surah_name}")
            # [Add playback logic here]
        except IndexError:
            await ctx.send("Invalid surah number. Please use `?list` to see available surahs.", delete_after=10)

async def setup(bot):
    await bot.add_cog(Public(bot))
