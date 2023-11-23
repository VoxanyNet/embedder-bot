import requests as r

class UnknownPostType(Exception):
    pass 

class Post:
    
    def __init__(self, url: str) -> None:
        self.url = url

        self.session = r.Session()

        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
            }   
        )

    def fetch_media_url(self) -> str:
        
        if "picture" not in self.url and "video" not in self.url:

            raise UnknownPostType(f"unknown post type for url {self.url}")

        html = self.session.get(self.url).text

        media_url_begin_index = html.find("https://img.ifunny.co")

        # this will give the index relative to the beginning of the media url
        media_url_end_index = html[media_url_begin_index: ].find('"')

        return html[media_url_begin_index : media_url_begin_index + media_url_end_index]