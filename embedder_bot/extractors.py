import os
import json

import yt_dlp
import requests

from embedder_bot import utils

class FailedToExtract(Exception):
    pass 

class Extractor:
    def extract_media_url(self) -> str:
        """
        Extract direct link to media
        """

        raise NotImplementedError()

class HTMLExtractor(Extractor):
    def __init__(self, url: str):

        self.url = url
        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
            }   
        )


class YTDLExtractor(Extractor):

    def __init__(self, url: str):
        
        self.url = url 

        self.yt_dlp_options = {
            "quiet": True
        }
    
    def _extract_info(self):
        
        with yt_dlp.YoutubeDL(self.yt_dlp_options) as yt:
            return yt.extract_info(self.url, download=False)


class IFunny(HTMLExtractor):

    def extract_media_url(self) -> str:
        
        html = self.session.get(self.url).text

        media_url_begin_index = html.find("https://img.ifunny.co")

        # this will give the index relative to the beginning of the media url
        media_url_end_index = html[media_url_begin_index: ].find('"')

        media_url = html[media_url_begin_index : media_url_begin_index + media_url_end_index]

        return media_url

class TikTok(YTDLExtractor):

    def extract_media_url(self) -> str: 

        info = self._extract_info()

        format = utils.find_one(
            {
                "format_note": "Direct video (API)"
            },
            info["formats"]
        )

        if format is None:
            raise FailedToExtract()

        return format["url"]
    
URL_DOWNLOADER_MAP = {
    "ifunny.co": IFunny,
    "tiktok.com": TikTok
}

if __name__ == "__main__":
    extractor = TikTok("https://www.tiktok.com/@operagxofficial/video/7316135204190522656")

    extractor.extract_media_url()