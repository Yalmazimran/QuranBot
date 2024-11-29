import os
import discord
from discord.ext import commands
from googleapiclient.discovery import build
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Create a YouTube API client
def get_youtube_service():
    api_key = os.getenv("YOUTUBE_API_KEY")  # Load API key from environment variable
    if not api_key:
        logging.error("API Key is missing from the environment.")
        raise EnvironmentError("YOUTUBE_API_KEY is not set.")
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube
    except Exception as e:
        logging.error(f"Error creating YouTube service: {e}")
        raise

# Fetch playlist
async def fetch_playlist(playlist_id):
    youtube = get_youtube_service()
    
    video_links = []
    next_page_token = None
    
    while True:
        try:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,  # You can adjust this if needed
                pageToken=next_page_token
            )
            
            response = request.execute()
            
            # Collect video details
            for item in response["items"]:
                video_title = item["snippet"]["title"]
                video_url = f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
                video_links.append(f"{video_title}: {video_url}")
            
            # Check if there are more pages
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break  # Exit the loop if there's no next page
        
        except Exception as e:
            logging.error(f"Error fetching playlist: {e}")
            break  # Exit the loop if there's an error during the API request
    
    return video_links

class Public(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("Public cog initialized.")  # Logging to check if the cog is properly initialized

    @commands.command(name="surah_playlist")
    async def surah_playlist(self, ctx):
        playlist_id = "PLoqNzfHlA__knCeUoKUHjQfZpUL6mj64w"  # Replace with your YouTube playlist ID
        try:
            video_links = await fetch_playlist(playlist_id)
            if not video_links:
                await ctx.send("No videos found in the playlist.")
                return
            
            # Format the playlist (limit to 2000 characters per Discord message)
            playlist_message = "\n".join(video_links)
            if len(playlist_message) > 2000:
                # Split the message into chunks if it exceeds Discord's 2000-character limit
                chunks = [playlist_message[i:i + 2000] for i in range(0, len(playlist_message), 2000)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(f"Here is the Surah playlist:\n{playlist_message}")
        
        except Exception as e:
            logging.error(f"Error sending playlist to Discord: {e}")
            await ctx.send("There was an error fetching the playlist.")

# Setup method to add the cog - This line **must not be awaited**
def setup(bot):
    bot.add_cog(Public(bot))  # This should NOT be awaited










