# enrich_books.py
import json
import re
from duckduckgo_search import DDGS
import time
import argparse

DEFAULT_INPUT = "kindle_books_parsed.json"
DEFAULT_OUTPUT = "kindle_books_enriched.json"

def find_amazon_url(title, author):
    query = f"{title} {author} Amazon"
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            url = r.get("href", "") or r.get("url", "")
            if "amazon.com" in url and "/dp/" in url:
                m = re.search(r"/dp/([A-Z0-9]{10})", url)
                if m:
                    return url.split("?")[0], m.group(1)
    return None, None

def enrich_books(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        books = json.load(f)

        for book in books:
            print(f"Enriching: {book.get('title', '')} by {book.get('author', '')}")
            try:
                url, asin = find_amazon_url(book["title"], book["author"])
                book["amazon_url"] = url or ""
                book["asin"] = asin or ""
            except Exception as e:
                print(f"Error on {book['title']}: {e}")
                book["amazon_url"] = ""
                book["asin"] = ""
            time.sleep(3)


    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    print(f"\nEnriched {len(books)} books. Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enrich book JSON with Amazon URL and ASIN.")
    parser.add_argument('--input', type=str, default=DEFAULT_INPUT, help="Input JSON file (default: kindle_books_parsed.json)")
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT, help="Output JSON file (default: kindle_books_enriched.json)")
    args = parser.parse_args()

    enrich_books(args.input, args.output)
