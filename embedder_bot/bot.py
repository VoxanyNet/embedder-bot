from typing import Dict, Type
import uuid

import discord

from embedder_bot import extractors
from embedder_bot import shlink
from embedder_bot import commands

class EmbedderBot(discord.Bot):
    def __init__(self, shlink_url: str, shlink_api_key: str, download_folder: str, description=None, *args, **options):

        self.download_folder = download_folder

        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(description, intents=intents, *args, **options)
        
        # the original message id, our reply with the media link
        self.reply_messages: Dict[int, int] = {}

        self.add_listener(self.fetch_media_link, "on_message")
        self.add_listener(self.delete_reply, "on_message_delete")

        self.add_application_command(commands.ping)

        self.shlink = shlink.Shlink(url=shlink_url, api_key=shlink_api_key)

    async def fetch_media_link(self, message: discord.Message):
        
        # can_embed = False 

        # for role in message.author.roles:
        #     if role.permissions.embed_links:
        #         can_embed = True
            
        #     if role.permissions.attach_files:
        #         can_attatch = True
        
        # if not can_embed or not can_attatch:

        #     return
        
        # check if link has an extractor
        extractor_class: Type[extractors.Extractor] = None 

        for supported_url_base, link_extractor in extractors.URL_DOWNLOADER_MAP.items():
            if supported_url_base in message.content:

                extractor_class = link_extractor

                break
        
        # if we can't find an extractor for this link
        if extractor_class == None:
            return 

        # this wont work if the message contains more than just a url
        extractor = extractor_class(url=message.content, download_folder=self.download_folder)

        media_url = await self.loop.run_in_executor(
            None,
            extractor.extract_media_url
        )

        # if we can't find a media url
        if media_url is None:
            return

        await message.channel.trigger_typing()

        file_extension = media_url.split(".")[-1]

        slug = f"{str(uuid.uuid4())[0:5]}.{file_extension}"
        
        shortened_media_url = await self.loop.run_in_executor(
            None,
            self.shlink.shorten_url,
            media_url,
            slug
        )

        reply_message = await message.reply(shortened_media_url)
        
        self.reply_messages[message.id] = reply_message.id
    
    async def delete_reply(self, message: discord.Message):

        try:
            reply_id = self.reply_messages[message.id]
        except KeyError:
            return 
        
        reply_message = await message.channel.fetch_message(reply_id)
        
        await reply_message.delete()

        

