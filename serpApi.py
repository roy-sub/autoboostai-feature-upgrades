import json
import requests
from typing import Any, Dict
from urllib.parse import quote
from config import settings

class GoogleSearchClient:

    def __init__(self):
        self.base_url = 'https://api.brightdata.com/request'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.BRIGHTDATA_API_KEY}'
        }

    def search(self, keyword: str, page: int = 0) -> Dict[str, Any]:
        """Ask BrightData for Google results as parsed JSON (brd_json=1).

        Google no longer puts result links in the page HTML, so scraping
        <a> tags returns nothing. BrightData parses the SERP for us.
        """
        start = page * settings.RESULTS_PER_PAGE

        search_url = (
            f'https://www.google.com/search?q={quote(keyword)}'
            f'&start={start}'
            f'&num={settings.RESULTS_PER_PAGE}'
            f'&gl={settings.SERP_COUNTRY}'
            f'&hl={settings.SERP_LANGUAGE}'
            f'&brd_json=1'
        )

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
        return json.loads(response.text)
