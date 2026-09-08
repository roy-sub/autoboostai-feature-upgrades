import json
from typing import Any, Dict, List
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from constants import EXCLUDE_WORDS, EXCLUDE_DOMAINS

def _clean_domain(raw: str) -> str:
    """Turn a display_link into a plain 'https://host' base url, or ''.

    Handles breadcrumb tails such as:
        'https://huisartsenpostenamsterdam.nl > praktijk > contact'
    and applies the EXCLUDE_WORDS / EXCLUDE_DOMAINS filters.
    """
    if not raw:
        return ''

    # strip breadcrumb tail: Google uses the U+203A single angle quote
    raw = raw.split('›')[0].split('>')[0].strip()
    if not raw:
        return ''

    if not raw.startswith(('http://', 'https://')):
        raw = f'https://{raw}'

    try:
        parsed = urlparse(raw)
    except Exception:
        return ''

    if not parsed.netloc or parsed.netloc == '.com':
        return ''

    check_domain = parsed.netloc.lower().removeprefix('www.')

    if any(word in check_domain for word in EXCLUDE_WORDS):
        return ''

    if check_domain in EXCLUDE_DOMAINS:
        return ''

    return f"{parsed.scheme}://{parsed.netloc}".rstrip('/')

def extract_domains_from_serp_json(data: Any) -> List[str]:
    """Pull website domains out of BrightData's parsed SERP JSON.

    The 'link' field is a google.com/goto redirect - the real site is in
    'display_link', so that is what we read.
    """
    if not data:
        return []

    if isinstance(data, (str, bytes)):
        try:
            data = json.loads(data)
        except Exception:
            return []

    if not isinstance(data, dict):
        return []

    domains = set()

    for item in data.get('organic') or []:
        if not isinstance(item, dict):
            continue
        base_url = _clean_domain(item.get('display_link') or '')
        if base_url:
            domains.add(base_url)

    return list(domains)

def extract_domains_from_raw_html(html: str) -> List[str]:
    """Legacy HTML scraper.

    Kept so nothing that still imports it breaks, but Google no longer
    exposes result links in the HTML - this returns [] on live SERPs.
    Use extract_domains_from_serp_json instead.
    """
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

        base_url = _clean_domain(url)
        if base_url:
            domains.add(base_url)

    return list(domains)

def convert_domain_list(domain_list: List[str]) -> List[Dict[str, str]]:
    result = []
    for domain in domain_list:
        if not domain.startswith(('http://', 'https://')):
            domain = f'https://{domain}'
        result.append({"domain": domain})
    return result
