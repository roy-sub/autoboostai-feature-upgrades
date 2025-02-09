import re
from typing import List, Set
import time
from dynamoDB import DomainUrlManager
from serpApi import GoogleSearchClient
from used_domain_fetcher import DomainFetcher
from extractUrl import extract_domains_from_raw_html, convert_domain_list

class URLGenerator:
    
    def __init__(self, 
                 domain_fetcher: DomainFetcher = None,
                 domain_manager: DomainUrlManager = None,
                 search_client: GoogleSearchClient = None):

        self.domain_fetcher = domain_fetcher or DomainFetcher()
        self.domain_manager = domain_manager or DomainUrlManager()
        self.search_client = search_client or GoogleSearchClient()
        self.TARGET_URLS = 50
        self.MAX_PAGES = 25

    def generate_urls(self, user_id: str, search_keyword: str) -> List[str]:

        try:
            # Get used domains for the user
            try:
                used_domains = set(self.domain_fetcher.get_domain_urls(user_id))
            except Exception:
                used_domains = set()
            
            # Get existing domains for the keyword from DynamoDB
            try:
                existing_domains = set(self.domain_manager.get_domain_urls(search_keyword))
            except KeyError:
                existing_domains = set()
            
            # Create first set: domains in database but not used by user
            available_domains = existing_domains - used_domains
            
            # Calculate how many more domains we need
            remaining_count = self.TARGET_URLS - len(available_domains)

            new_domains = set()
            page = 0
            max_pages = self.MAX_PAGES

            count_empty_page = 0
            previous_page_empty = False  # Track if previous page was empty
            
            while len(new_domains) < remaining_count and page < max_pages:

                # Add delay between requests
                time.sleep(5)
                
                serp_html = self.search_client.search(search_keyword, page)
                
                # Extract domains from the page
                current_page_domains = extract_domains_from_raw_html(serp_html)

                # Series of Consecutive Empty Pages Check
                current_page_empty = not bool(current_page_domains)
                
                if previous_page_empty and current_page_empty:
                    count_empty_page += 1
                    if count_empty_page >= 5: 
                        break
                elif not current_page_empty:
                    count_empty_page = 0
                
                previous_page_empty = current_page_empty
                
                # Filter out domains that are either in used_domains or available_domains
                domains_to_add = {
                    domain for domain in current_page_domains 
                    if domain not in used_domains and domain not in available_domains
                }
                
                # Add new domains to the set
                new_domains.update(domains_to_add)
                
                page += 1

            # Add to dynamodb against the keyword
            try:
                self.domain_manager.add_domain_urls(search_keyword, new_domains)
            except Exception:
                pass  # Ignore any errors and proceed

            # Combine available and new domains
            final_domains = list(available_domains.union(new_domains))

            # Converting Domain List
            result = convert_domain_list(final_domains)

            # Return only the required number of domains
            return result
            
        except Exception as e:
            return []
