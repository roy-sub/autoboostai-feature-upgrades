import requests
from typing import List
from config import settings

class DomainFetcher:
    
    def __init__(self):
        self.endpoint = f"{settings.N8N_WEBHOOK_BASE_URL}/get_used_website_urls"
    
    def get_domain_urls(self, record_id: str) -> List[str]:
        try:
            response = requests.get(
                self.endpoint,
                params={'id': record_id},
                timeout=settings.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            return [item.get('domain-url', '') for item in data if item.get('domain-url')]
        except (requests.RequestException, KeyError, ValueError):
            return []
