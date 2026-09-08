import time

from generator import URLGenerator

if __name__ == "__main__":

    # SEARCH INPUT - edit these two values
    USER_ID = "recTvHvu7ZX11Wt1H"
    SEARCH_KEYWORD = "Doctors in Amsterdam"

    print("=" * 70)
    print("  /get-website-domains  |  pipeline test")
    print("=" * 70)
    print(f"user_id        : {USER_ID}")
    print(f"search_keyword : {SEARCH_KEYWORD}")
    print("-" * 70)

    # --- same validation as the API endpoint (app.py::generate_domains) ---
    if not USER_ID or not SEARCH_KEYWORD:
        raise SystemExit("[400] user_id and search_keyword are required")

    search_keyword = SEARCH_KEYWORD.strip()
    if len(search_keyword) < 2:
        raise SystemExit("[400] search_keyword must be at least 2 characters")

    # --- same call as the API endpoint ---
    url_generator = URLGenerator()

    start = time.time()
    try:
        domains = url_generator.generate_urls(USER_ID, search_keyword)
        domains = domains if domains else []
    except Exception as e:
        raise SystemExit(f"[500] Error generating domains: {e}")
    elapsed = time.time() - start

    # --- print the response exactly as the endpoint would return it ---
    print("-" * 70)
    print(f"Status         : 200 OK")
    print(f"Elapsed        : {elapsed:.2f}s")
    print(f"Total domains  : {len(domains)}")
    print("-" * 70)

    if not domains:
        print("No domains returned (empty list).")
    else:
        for i, item in enumerate(domains, start=1):
            print(f"{i:>3}. {item['domain']}")

    print("=" * 70)
    print("Raw response payload:")
    print(domains)
