import requests
from typing import List

class DomainFetcher:
    
    def __init__(self, base_url: str = "https://ws-ai.app.n8n.cloud/webhook"):

        self.base_url = base_url
        self.endpoint = f"{self.base_url}/get_used_website_urls"
    
    def get_domain_urls(self, record_id: str) -> List[str]:

        try:
            # Make the request
            response = requests.get(
                self.endpoint,
                params={'id': record_id},
                timeout=30  # 30 second timeout
            )
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Parse the JSON response
            data = response.json()
            
            # Extract domain URLs from the response
            domain_urls = [item['domain-url'] for item in data]
            
            return domain_urls
            
        except (requests.RequestException, KeyError, ValueError) as e:
            print(f'Error fetching domain URLs: {e}')
            return []
