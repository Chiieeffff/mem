"""
Web search tool using Tavily API.
Usage: python tools/search_web.py --queries '["query1", "query2"]'
Output: JSON array of {query, results: [{title, url, content}]} to stdout
"""

import argparse
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def search(queries: list[str], max_results: int = 5) -> list[dict]:
    try:
        from tavily import TavilyClient
    except ImportError:
        print("Error: tavily-python not installed. Run: pip install tavily-python", file=sys.stderr)
        sys.exit(1)

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("Error: TAVILY_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    client = TavilyClient(api_key=api_key)
    output = []

    for query in queries:
        try:
            response = client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced",
                include_raw_content=False,
            )
            results = [
                {"title": r.get("title", ""), "url": r.get("url", ""), "content": r.get("content", "")}
                for r in response.get("results", [])
            ]
            output.append({"query": query, "results": results})
        except Exception as e:
            output.append({"query": query, "error": str(e), "results": []})

    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", required=True, help="JSON array of search query strings")
    parser.add_argument("--max-results", type=int, default=5)
    args = parser.parse_args()

    try:
        queries = json.loads(args.queries)
    except json.JSONDecodeError as e:
        print(f"Error: --queries must be a valid JSON array: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(queries, list):
        print("Error: --queries must be a JSON array", file=sys.stderr)
        sys.exit(1)

    results = search(queries, max_results=args.max_results)
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
