import time
from typing import List, Set
from concurrent.futures import ThreadPoolExecutor
from dynamoDB import DomainUrlManager
from serpApi import GoogleSearchClient
from usedDomainFetcher import DomainFetcher
from extractUrl import extract_domains_from_serp_json, sanitize_domains, convert_domain_list
from config import settings

class URLGenerator:
    
    def __init__(self):
        self.domain_fetcher = DomainFetcher()
        self.domain_manager = DomainUrlManager()
        self.search_client = GoogleSearchClient()

    def _fetch_used_domains(self, user_id: str) -> Set[str]:
        try:
            return set(self.domain_fetcher.get_domain_urls(user_id))
        except Exception:
            return set()

    def _fetch_existing_domains(self, search_keyword: str) -> Set[str]:
        try:
            stored = self.domain_manager.get_domain_urls(search_keyword)
        except Exception:
            return set()
        
        # The cache is not trusted blindly: rows written by older versions
        # can hold junk, and the exclude lists may have changed since.
        clean = sanitize_domains(stored)
        
        dropped = len(stored) - len(clean)
        if dropped > 0:
            # [LOG] cached entries that no longer pass the rules
            print(f"[DB] Ignored {dropped} invalid/excluded cached entries")
        
        return set(clean)

    def _fetch_serp_domains(
        self, 
        search_keyword: str, 
        remaining_count: int, 
        used_domains: Set[str], 
        available_domains: Set[str]
    ) -> Set[str]:
        new_domains: Set[str] = set()
        page = 0
        consecutive_empty = 0
        consecutive_no_new = 0
        
        while len(new_domains) < remaining_count and page < settings.MAX_PAGES:
            if page > 0:
                time.sleep(settings.SERP_DELAY)
            
            try:
                serp_data = self.search_client.search(search_keyword, page)
                current_domains = extract_domains_from_serp_json(serp_data)
                
                if not current_domains:
                    consecutive_empty += 1
                    if consecutive_empty >= 5:
                        break
                else:
                    consecutive_empty = 0
                    
                filtered = {
                    d for d in current_domains 
                    if d not in used_domains and d not in available_domains and d not in new_domains
                }
                new_domains.update(filtered)
                
                # Google has run out of fresh results - stop paging instead
                # of burning SERP_DELAY on pages that just repeat themselves.
                if filtered:
                    consecutive_no_new = 0
                else:
                    consecutive_no_new += 1
                    if consecutive_no_new >= settings.MAX_PAGES_WITHOUT_NEW:
                        break
                
            except Exception:
                consecutive_empty += 1
                if consecutive_empty >= 5:
                    break
            
            page += 1
        
        if len(new_domains) < remaining_count:
            # [LOG] Google simply did not have this many distinct sites
            print(f"[SERP] Exhausted results at page {page}: found "
                  f"{len(new_domains)} of {remaining_count} requested")
        
        return new_domains

    def generate_urls(self, user_id: str, search_keyword: str) -> List[dict]:
        try:
            with ThreadPoolExecutor(max_workers=2) as executor:
                future_used = executor.submit(self._fetch_used_domains, user_id)
                future_existing = executor.submit(self._fetch_existing_domains, search_keyword)
                
                used_domains = future_used.result()
                existing_domains = future_existing.result()
            
            available_domains = existing_domains - used_domains
            remaining_count = settings.TARGET_URLS - len(available_domains)
            
            new_domains: Set[str] = set()
            if remaining_count > 0:
                # [LOG] Extracting from web - not enough in database
                print(f"[SERP] Extracting {remaining_count} domains from web for: {search_keyword}")
                
                new_domains = self._fetch_serp_domains(
                    search_keyword, remaining_count, used_domains, available_domains
                )
                
                if new_domains:
                    try:
                        self.domain_manager.add_domain_urls(search_keyword, list(new_domains))
                        # [LOG] Saved to database
                        print(f"[DB] Saved {len(new_domains)} new domains to database")
                    except Exception:
                        pass
            else:
                # [LOG] Found sufficient domains in database
                print(f"[DB] Found {len(available_domains)} domains in database - skipping web extraction")
            
            final_domains = list(available_domains | new_domains)[:settings.TARGET_URLS]
            return convert_domain_list(final_domains)
            
        except Exception:
            return []
