import uuid
import os

import yt_dlp
import requests as r

class FailedToDownload(Exception):
    pass

class Downloader:
    def __init__(self, url: str, output_directory: str, output_name: str = None):
        self.url = url
        self.output_directory = output_directory

        if output_name is None:
            output_name = str(uuid.uuid4())

        self.output_name = output_name
    
    def download(self) -> str:
        """
        Download post media and return file path
        """
        raise NotImplementedError()

class YTDLDownloader(Downloader):
    def __init__(self, url: str, output_directory: str, output_name: str = None):
        super().__init__(url, output_directory, output_name)

        self.yt_dlp_options = {
            "outtmpl": f"{self.output_directory}/{self.output_name}.%(ext)s",
            "quiet": True
        }  

    def download(self) -> str:

        with yt_dlp.YoutubeDL(self.yt_dlp_options) as yt:

            yt.download([self.url])
        
        # find full file path with extension
        for file in os.listdir(self.output_directory):
            if self.output_name in file:
                return os.path.abspath(f"{self.output_directory}/{file}")  
        
        raise FailedToDownload()

class IFunny(Downloader):
    def download(self) -> str:

        session = r.Session()

        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
            }   
        )
        
        html = session.get(self.url).text

        media_url_begin_index = html.find("https://img.ifunny.co")

        # this will give the index relative to the beginning of the media url
        media_url_end_index = html[media_url_begin_index: ].find('"')

        media_url = html[media_url_begin_index : media_url_begin_index + media_url_end_index]

        # download the image
        image_response = session.get(media_url)

        # extract filetype extension
        image_file_extension = image_response.headers["Content-Type"].split("/")[1]

        # construct file path
        file_path = f"{self.output_directory}/{self.output_name}.{image_file_extension}"

        # save image to file
        with open(file_path, "wb") as file:
            file.write(image_response.content)

        return file_path

class TikTok(YTDLDownloader):
    def download(self):
        return super().download()

class YouTube(YTDLDownloader):
    def download(self):
        return super().download()
    
class Twitter(YTDLDownloader):
    def download(self) -> str:
        return super().download()
    
URL_DOWNLOADER_MAP = {
    "ifunny.co": IFunny,
    "tiktok.com": TikTok,
    "youtube.com": YouTube,
    "twitter.com": Twitter
}