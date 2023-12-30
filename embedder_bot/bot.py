from typing import Dict, Type
import os
import tempfile

import discord

from embedder_bot import downloaders

class EmbedderBot(discord.Bot):
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
            
            if role.permissions.attach_files:
                can_attatch = True
        
        if not can_embed or not can_attatch:

            return
        
        # check if link exists in supported links dict
        # TODO: extract every link from message and download each one

        downloader: Type[downloaders.Downloader] = None 

        for supported_link, link_downloader in downloaders.URL_DOWNLOADER_MAP.items():
            if supported_link in message.content:

                downloader = link_downloader

                break
        
        # if we can't find a downloader for this link
        if downloader == None:
            return 
        
        await message.channel.trigger_typing()

        # this wont work if the message contains more than just a url
        dl = downloader(message.content, output_directory=tempfile.gettempdir())

        file_path = dl.download()

        # TODO: upload to file server if too large

        reply_message = await message.reply(file=discord.File(file_path))

        # TODO: add ability to convert file type if incompatible with discord's player

        os.remove(file_path)
        
        self.reply_messages[message.id] = reply_message.id
    
    async def delete_reply(self, message: discord.Message):

        try:
            reply_id = self.reply_messages[message.id]
        except KeyError:
            return 
        
        reply_message = await message.channel.fetch_message(reply_id)
        
        await reply_message.delete()

        

