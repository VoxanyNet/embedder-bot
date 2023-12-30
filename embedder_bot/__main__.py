import os

from embedder_bot import bot

DISCORD_TOKEN = os.environ["EMBEDDER_BOT_DISCORD_TOKEN"]
bot = bot.EmbedderBot()

bot.run(DISCORD_TOKEN)