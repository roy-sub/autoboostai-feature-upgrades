import re
from typing import List, Dict
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from constants import EXCLUDE_WORDS, EXCLUDE_DOMAINS

def extract_domains_from_raw_html(html: str) -> List[str]:

    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all <a> tags with href attributes
    links = soup.find_all('a', href=True)
    
    domains = set()
    for link in links:
        url = link['href']
        
        # Skip if not a valid URL
        if not url.startswith(('http://', 'https://')):
            continue
            
        try:
            # Parse URL
            parsed_url = urlparse(url)
            
            # Skip if netloc is empty or malformed
            if not parsed_url.netloc or parsed_url.netloc == '.com':
                continue
                
            # Reconstruct base URL without trailing slash
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            # Remove 'www.' from netloc for checking exclusions
            check_domain = re.sub(r'^www\.', '', parsed_url.netloc)
            
            # Skip if domain contains any excluded words
            if any(word in check_domain.lower() for word in EXCLUDE_WORDS):
                continue
                
            # Skip if domain is in excluded domains list
            if check_domain in EXCLUDE_DOMAINS:
                continue
                
            # Remove trailing slash if present
            base_url = base_url.rstrip('/')
            
            domains.add(base_url)
            
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            continue
    
    return list(domains)

def convert_domain_list(domain_list: List[str]) -> List[Dict[str, str]]:

    result = []
    
    for domain in domain_list:
        # If the domain doesn't start with http/https, add it
        if not domain.startswith(('http://', 'https://')):
            domain = f'https://{domain}'
            
        result.append({
            "domain": domain
        })
    
    return result
