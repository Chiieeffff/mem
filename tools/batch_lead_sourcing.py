"""
Batch lead sourcing tool for GatewayCrypto iGaming outreach.
Runs web searches and site scrapes in parallel for a list of companies.

Usage:
  python tools/batch_lead_sourcing.py --leads '[
    {"company": "SoftSwiss", "website": "https://softswiss.com", "contact": "John Doe"},
    {"company": "EveryMatrix", "website": "https://everymatrix.com"}
  ]'

Each lead entry requires "company". "website" and "contact" are optional.
Output: JSON array of {company, contact, website, search_results, scrape_results} to stdout.
"""

import argparse
import json
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()


def search_lead(company: str, contact: str | None) -> list[dict]:
    from tavily import TavilyClient

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY not set in .env")

    client = TavilyClient(api_key=api_key)

    queries = [
        f'"{company}" iGaming platform partner crypto payment 2024 2025',
        f'"{company}" CoinsPaid OR NowPayments OR BitPay OR Coinify OR Paycos',
        f'"{company}" Crunchbase funding employees headquarters',
        f'"{company}" iGaming license jurisdiction US players',
    ]
    if contact:
        queries.append(f'"{contact}" "{company}" LinkedIn')

    results = []
    for query in queries:
        try:
            response = client.search(
                query=query,
                max_results=3,
                search_depth="basic",
                include_raw_content=False,
            )
            hits = [
                {"title": r.get("title", ""), "url": r.get("url", ""), "content": r.get("content", "")}
                for r in response.get("results", [])
            ]
            results.append({"query": query, "results": hits})
        except Exception as e:
            results.append({"query": query, "error": str(e), "results": []})

    return results


def scrape_lead(website: str) -> dict:
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin, urlparse
    import re

    CANDIDATE_PATHS = ["/", "/about", "/partners", "/solutions", "/platform"]
    HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; research-bot/1.0)"}
    TIMEOUT = 10

    parsed = urlparse(website)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    pages = []

    for path in CANDIDATE_PATHS:
        url = urljoin(origin, path)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "head"]):
                tag.decompose()
            text = soup.get_text(separator=" ", strip=True)
            text = re.sub(r"\s{3,}", "  ", text)
            pages.append({"path": path, "text": text[:4000]})
        except Exception:
            continue

    return {"url": website, "pages": pages}


def process_lead(lead: dict) -> dict:
    company = lead.get("company", "").strip()
    contact = lead.get("contact", "").strip() or None
    website = lead.get("website", "").strip() or None

    result = {
        "company": company,
        "contact": contact,
        "website": website,
        "search_results": [],
        "scrape_results": None,
        "errors": [],
    }

    try:
        from tavily import TavilyClient
        result["search_results"] = search_lead(company, contact)
    except ImportError:
        result["errors"].append("tavily-python not installed")
    except Exception as e:
        result["errors"].append(f"Search failed: {e}")

    if website:
        try:
            import requests
            from bs4 import BeautifulSoup
            result["scrape_results"] = scrape_lead(website)
        except ImportError:
            result["errors"].append("requests/beautifulsoup4 not installed")
        except Exception as e:
            result["errors"].append(f"Scrape failed: {e}")

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--leads",
        required=True,
        help='JSON array of lead objects: [{"company": "...", "website": "...", "contact": "..."}]',
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)",
    )
    args = parser.parse_args()

    try:
        leads = json.loads(args.leads)
    except json.JSONDecodeError as e:
        print(f"Error: --leads must be a valid JSON array: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(leads, list) or not leads:
        print("Error: --leads must be a non-empty JSON array", file=sys.stderr)
        sys.exit(1)

    for i, lead in enumerate(leads):
        if not isinstance(lead, dict) or not lead.get("company"):
            print(f"Error: lead at index {i} must be an object with a 'company' field", file=sys.stderr)
            sys.exit(1)

    results = [None] * len(leads)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_index = {executor.submit(process_lead, lead): i for i, lead in enumerate(leads)}
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                results[idx] = {
                    "company": leads[idx].get("company", "unknown"),
                    "error": str(e),
                    "search_results": [],
                    "scrape_results": None,
                }

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
