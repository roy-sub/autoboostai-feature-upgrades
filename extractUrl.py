from typing import List, Dict
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from constants import EXCLUDE_WORDS, EXCLUDE_DOMAINS

def extract_domains_from_raw_html(html: str) -> List[str]:
    if not html:
        return []
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except Exception:
        return []
    
    domains = set()
    
    for link in soup.find_all('a', href=True):
        url = link['href']
        
        if not url.startswith(('http://', 'https://')):
            continue
        
        try:
            parsed = urlparse(url)
            
            if not parsed.netloc or parsed.netloc == '.com':
                continue
            
            check_domain = parsed.netloc.lower().removeprefix('www.')
            
            if any(word in check_domain for word in EXCLUDE_WORDS):
                continue
            
            if check_domain in EXCLUDE_DOMAINS:
                continue
            
            base_url = f"{parsed.scheme}://{parsed.netloc}".rstrip('/')
            domains.add(base_url)
            
        except Exception:
            continue
    
    return list(domains)

def convert_domain_list(domain_list: List[str]) -> List[Dict[str, str]]:
    result = []
    for domain in domain_list:
        if not domain.startswith(('http://', 'https://')):
            domain = f'https://{domain}'
        result.append({"domain": domain})
    return result
