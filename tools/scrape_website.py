"""
Website scraper tool using requests + BeautifulSoup.
Fetches homepage and common sub-pages (/about, /partners, /solutions, /platform, /features).
Usage: python tools/scrape_website.py --url https://example.com
Output: JSON {url, pages: [{path, text}]} to stdout
"""

import argparse
import json
import sys
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: requests and beautifulsoup4 are required. Run: pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)

CANDIDATE_PATHS = ["/", "/about", "/partners", "/solutions", "/platform", "/features", "/integrations"]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; research-bot/1.0)"}
TIMEOUT = 10


def fetch_page(url: str) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "head"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        # Collapse whitespace
        import re
        text = re.sub(r"\s{3,}", "  ", text)
        return text[:8000]  # Cap per page to keep output manageable
    except Exception:
        return None


def scrape(base_url: str) -> dict:
    parsed = urlparse(base_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    pages = []

    for path in CANDIDATE_PATHS:
        url = urljoin(origin, path)
        text = fetch_page(url)
        if text:
            pages.append({"path": path, "text": text})

    return {"url": base_url, "pages": pages}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Company website URL to scrape")
    args = parser.parse_args()

    result = scrape(args.url)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
