import json
import time
from typing import Dict

import requests as r
import discord
from discord.ext import tasks

from ifunnybot.ifunny import Post

class IFunnyBot(discord.Bot):
    def __init__(self, description=None, *args, **options):

        intents = discord.Intents.default()

        intents.message_content = True

        super().__init__(description, intents=intents, *args, **options)
        
        # the original message id, our reply with the media link
        self.reply_messages: Dict[int, int] = {}

        self.add_listener(self.fetch_media_link, "on_message")
        self.add_listener(self.delete_reply, "on_message_delete")
    
    async def fetch_media_link(self, message: discord.Message):
        
        can_embed = False 

        for role in message.author.roles:
            if role.permissions.embed_links:
                can_embed = True
        
        if not can_embed:
            return
        
        if "https://ifunny.co/" not in message.content:
            return

        media_url = Post(message.content).fetch_media_url()

        reply_message = await message.reply(media_url)

        self.reply_messages[message.id] = reply_message.id
    
    async def delete_reply(self, message: discord.Message):

        try:
            reply_id = self.reply_messages[message.id]
        except KeyError:
            return 
        
        reply_message = await message.channel.fetch_message(reply_id)
        
        await reply_message.delete()

        

