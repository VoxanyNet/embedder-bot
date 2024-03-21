from typing import Optional

import requests

class Shlink:
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key
    
    def shorten_url(self, url: str, slug: Optional[str] = None) -> str:

        request_body = {
            "longUrl": url,
            "crawlable": False,
            "forwardQuery": True,
            "findIfExists": False   
        }

        if slug: request_body["customSlug"] = slug

        response = requests.post(
            f"{self.url}/rest/v3/short-urls",
            headers={
                "X-Api-Key": self.api_key
            },
            json=request_body
        )

        response.raise_for_status()

        return response.json()["shortUrl"]