import os

from embedder_bot import bot

DISCORD_TOKEN = os.environ["BOT_DISCORD_TOKEN"]
SHLINK_URL = "https://" + os.environ["SHLINK_DOMAIN"]
SHLINK_API_KEY = os.environ["SHLINK_API_KEY"]
DOWNLOAD_FOLDER = os.environ["EMBEDDER_DOWNLOAD_FOLDER"]

bot = bot.EmbedderBot(shlink_url=SHLINK_URL, shlink_api_key=SHLINK_API_KEY, download_folder=DOWNLOAD_FOLDER)

bot.run(DISCORD_TOKEN)