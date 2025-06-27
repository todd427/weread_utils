# kindle_to_json.py

import json
import argparse
import re
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

    # Each product is usually within a div with class 'a-fixed-left-grid-inner' or 'a-row'
    for order_block in soup.find_all("div", class_="a-fixed-left-grid-inner"):
        # Find the title: typically an <a> tag with 'a-link-normal' and 'a-text-bold'
        title_tag = order_block.find("a", class_="a-link-normal")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)

        # Try to find the author (usually in a <span> with 'a-size-small' or after 'by ')
        author = None
        # Try to find a line with "by Author Name"
        byline = order_block.find("span", string=re.compile(r"^by "))
        if byline:
            author = byline.get_text(strip=True).replace("by ", "")
        else:
            # Sometimes it's in the next sibling text after title
            possible_author = title_tag.find_next(string=re.compile(r"by "))
            if possible_author:
                author = possible_author.strip().replace("by ", "")

        # Fallback: Kindle books with no author—mark as 'Kindle Edition' or skip if too junky
        if not author:
            # Kindle Unlimited etc, skip junk entries
            continue

        # Filter out non-book/junk titles (optional, customize as needed)
        junk = [
            "cover", "review", "invoice", "subscribe", "return", "replacement",
            "view order details", "ad free", "prime video"
        ]
        if any(j in title.lower() for j in junk):
            continue

        books.append({"title": title, "author": author})

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(books)} books from {args.input} and wrote output to {args.output}")

if __name__ == "__main__":
    main()

        # Fallback: look for next sibling "by ...", or just mark as 'Unknown'
