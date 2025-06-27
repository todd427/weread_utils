# kindle_to_json.py
import json
import argparse
from bs4 import BeautifulSoup

def main():
    parser = argparse.ArgumentParser(
        description="Extract book titles from Amazon Orders HTML to JSON."
    )
    parser.add_argument("--input", "-i", required=True, help="Input Amazon Orders HTML file")
    parser.add_argument("--output", "-o", required=True, help="Output JSON file")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    books = []
    seen = set()
    for tag in soup.find_all("a", class_="a-link-normal"):
        title = tag.get_text(strip=True)
        # Filter out junk/non-books
        if len(title) < 10:
            continue
        blacklist = [
            "order", "invoice", "return", "details", "prime", "subscribe",
            "review", "replacement", "your items", "view order"
        ]
        if any(x in title.lower() for x in blacklist):
            continue
        if title in seen:
            continue
        seen.add(title)
        # Set author as Unknown, unless you want to search more nearby
        books.append({"title": title, "author": "Unknown"})

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(books)} books from {args.input} and wrote output to {args.output}")

if __name__ == "__main__":
    main()
