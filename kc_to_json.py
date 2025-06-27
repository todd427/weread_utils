#!/usr/bin/env python3
"""
kc_to_json.py

Extracts book title and author information from Amazon Kindle "Manage Your Content and Devices" HTML exports.

USAGE:
    python kc_to_json.py KC01.htm [KC02.htm ...] > books.json

Requires: beautifulsoup4

Example:
    python kc_to_json.py KC01.htm > books.json
"""

import argparse
import sys
import json
from bs4 import BeautifulSoup

def parse_kindle_html(file_path):
    with open(file_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    books = []
    for title_div in soup.find_all("div", class_="digital_entity_title"):
        # Get the unique BOOKID from id attribute
        title_id = title_div.get("id")
        if not title_id or not title_id.startswith("content-title-"):
            continue
        book_id = title_id.replace("content-title-", "")

        # Extract the book title (inside nested div)
        heading_div = title_div.find("div", role="heading")
        title = heading_div.get_text(strip=True) if heading_div else None

        # Find corresponding author by book_id
        author_div = soup.find("div", id=f"content-author-{book_id}")
        author = author_div.get_text(strip=True) if author_div else None

        # Compose record
        book = {"title": title or "", "author": author or ""}
        books.append(book)
    return books

def main():
    parser = argparse.ArgumentParser(
        description="Extract book title and author info from Amazon Kindle Content & Devices HTML export."
    )
    parser.add_argument(
        "files", metavar="HTML", type=str, nargs="+",
        help="One or more exported Amazon Kindle HTML files (KC01.htm, KC02.htm, ...)"
    )
    args = parser.parse_args()

    all_books = []
    for file_path in args.files:
        try:
            books = parse_kindle_html(file_path)
            all_books.extend(books)
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)

    print(json.dumps(all_books, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
