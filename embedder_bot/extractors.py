import json
from typing import Optional
import os
import uuid

import yt_dlp
import requests

from embedder_bot import utils

class Extractor:
    def __init__(self, url: str, download_folder: str) -> Optional[str]:
        """
        Extract direct link to media
        """
        self.url = url
        self.download_folder = download_folder

class HTMLExtractor(Extractor):
    def __init__(self, url: str, download_folder: str):
        super().__init__(url=url, download_folder=download_folder)

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
            }   
        )


class YTDLExtractor(Extractor):

    def __init__(self, url: str, download_folder: str):
        
        super().__init__(url=url, download_folder=download_folder)

        self.yt_dlp_options = {
            "quiet": True
        }
    
    def _extract_info(self):
        
        with yt_dlp.YoutubeDL(self.yt_dlp_options) as yt:
            info = yt.extract_info(self.url, download=False)

            return info
    
    def extract_media_url(self) -> Optional[str]: 

        media_id = uuid.uuid4()
        
        try:
            query_params_index = self.url.index("?")

            url_no_query_params=self.url[0:query_params_index]

        except ValueError:
            url_no_query_params = self.url


        os.system(f"yt-dlp -o '{self.download_folder}/{media_id}.%(ext)s' {url_no_query_params}")

        media_file_path = None

        # find full file path including the extension
        for file in os.listdir(self.download_folder):

            print(file)
            if file.startswith(str(media_id)):

                media_file_path = file

                break
        
        if media_file_path == None:
            print("failed to find full media file path")

            return None
        
        media_url = f"https://dl.vxny.io/1176336161816461372/{media_file_path}"

        return media_url


class IFunny(HTMLExtractor):

    def extract_media_url(self) -> Optional[str]:
        
        html = self.session.get(self.url).text

        media_url_begin_index = html.find("https://img.ifunny.co")

        # this will give the index relative to the beginning of the media url
        media_url_end_index = html[media_url_begin_index: ].find('"')

        media_url = html[media_url_begin_index : media_url_begin_index + media_url_end_index]

        return media_url

class TikTok(YTDLExtractor):
    pass

class Twitter(YTDLExtractor):
    pass

class YoutubeShorts(YTDLExtractor):
    pass
    
URL_DOWNLOADER_MAP = {
    "ifunny.co": IFunny,
    "tiktok.com": TikTok,
    "twitter.com": Twitter,
    "youtube.com/shorts": YoutubeShorts,
    "x.com": Twitter
}