import requests
from urllib.parse import quote
from config import settings

class GoogleSearchClient:

    def __init__(self):
        self.base_url = 'https://api.brightdata.com/request'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.BRIGHTDATA_API_KEY}'
        }
    
    def search(self, keyword: str, page: int = 0) -> str:
        start = page * 10
        search_url = f'https://www.google.com/search?q={quote(keyword)}&start={start}'
        
        payload = {
            'zone': settings.BRIGHTDATA_ZONE,
            'url': search_url,
            'format': 'raw'
        }
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=payload,
            timeout=settings.REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.text
