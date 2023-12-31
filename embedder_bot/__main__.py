import os

from embedder_bot import bot

DISCORD_TOKEN = os.environ["BOT_DISCORD_TOKEN"]
SHLINK_URL = os.environ["SHLINK_DOMAIN"]
SHLINK_API_KEY = os.environ["SHLINK_API_KEY"]

bot = bot.EmbedderBot(shlink_url=SHLINK_URL, shlink_api_key=SHLINK_API_KEY)

bot.run(DISCORD_TOKEN)