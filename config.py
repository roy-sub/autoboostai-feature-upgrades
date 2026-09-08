import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY: str = os.getenv("API_KEY", "")
    BRIGHTDATA_API_KEY: str = os.getenv("BRIGHTDATA_API_KEY", "")
    BRIGHTDATA_ZONE: str = os.getenv("BRIGHTDATA_ZONE", "autoboostai_serp_api")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "eu-central-1")
    DYNAMODB_TABLE_NAME: str = os.getenv("DYNAMODB_TABLE_NAME", "autoboostai_domain_urls_table")
    N8N_WEBHOOK_BASE_URL: str = os.getenv("N8N_WEBHOOK_BASE_URL", "https://ws-ai.app.n8n.cloud/webhook")
    TARGET_URLS: int = 50
    MAX_PAGES: int = 25
    MAX_PAGES_WITHOUT_NEW: int = 3
    REQUEST_TIMEOUT: int = 30
    SERP_DELAY: float = 5.0
    RESULTS_PER_PAGE: int = 20
    SERP_COUNTRY: str = os.getenv("SERP_COUNTRY", "nl")
    SERP_LANGUAGE: str = os.getenv("SERP_LANGUAGE", "en")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
