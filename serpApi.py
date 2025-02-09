import requests
from urllib.parse import quote

class GoogleSearchClient:

    def __init__(self):

        self.api_key = "0bb882dffb293a2f7b54ab86aa23de9aac4694a243ef21d0851c64ee8b4cc004"
        self.base_url = 'https://api.brightdata.com/request'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer 0bb882dffb293a2f7b54ab86aa23de9aac4694a243ef21d0851c64ee8b4cc004'
        }
    
    def search(self, keyword: str, page: int = 0) -> str:

        # Calculate start parameter for pagination (Google uses multiples of 10)
        start = page * 10
        
        # Construct and encode the search URL
        search_url = f'https://www.google.com/search?q={quote(keyword)}&start={start}'
        
        # Prepare the request payload
        payload = {
            'zone': 'autoboostai_serp_api',
            'url': search_url,
            'format': 'raw'
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.text
            
        except requests.exceptions.RequestException as e:
            print(f'Error fetching search results: {e}')
            raise
