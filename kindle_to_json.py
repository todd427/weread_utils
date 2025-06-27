# kindle_to_json.py
import json
import argparse
from bs4 import BeautifulSoup

def main():
    parser = argparse.ArgumentParser(
        description="Extract book titles/authors from Amazon Orders HTML to JSON."
    )
    parser.add_argument("--input", "-i", required=True, help="Input Amazon Orders HTML file")
    parser.add_argument("--output", "-o", required=True, help="Output JSON file")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    books = []
    seen = set()
    # Robust blacklist to avoid junk links and navigation
    blacklist = [
        "order", "invoice", "return", "details", "prime", "subscribe",
        "review", "replacement", "your items", "view order", "account",
        "click here", "report the bug", "amazon pay", "not yet shipped",
        "recalls", "safety alerts", "your account", "opt in", "cart",
        "wishlist", "gift card", "customer service", "sell", "best sellers",
        "your orders", "your lists", "your rec", "your recalls",
        "sign in", "start here", "gift registry", "music", "fresh", "pantry",
        "prime video", "today's deals", "find a gift", "computers", "electronics",
        "books", "fashion", "coupons", "pharmacy", "beauty", "toys", "home", "sports"
    ]

    for tag in soup.find_all("a", class_="a-link-normal"):
        title = tag.get_text(strip=True)
        if len(title) < 10:
            continue
        if any(x in title.lower() for x in blacklist):
            continue
        if title in seen:
            continue
        seen.add(title)

        # Author extraction
        author = "Unknown"
        next_row = tag.find_parent("div", class_="a-row")
        if next_row:
            possible = []
            sib = next_row.find_next_siblings("div", class_="a-row")
            for s in sib:
                for span in s.find_all("span", class_="a-size-small"):
                    val = span.get_text(strip=True)
                    if "kindle edition" in val.lower():
                        continue
                    if val:
                        possible.append(val)
            if possible:
                author = possible[0]

        books.append({"title": title, "author": author})

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(books)} books from {args.input} and wrote output to {args.output}")

if __name__ == "__main__":
    main()

