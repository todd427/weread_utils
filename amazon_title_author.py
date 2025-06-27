# amazon_title_author.py
import json
import argparse
import urllib.parse
import re

def clean_title_for_search(title):
    # Remove parenthetical/bracketed content and some punctuation
    title = re.sub(r"\(.*?\)", "", title)
    title = re.sub(r"\[.*?\]", "", title)
    title = re.sub(r"[:;\"'‐–—-]", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip()

def main():
    parser = argparse.ArgumentParser(description="Add smart Amazon search URLs to every book entry.")
    parser.add_argument('--input', type=argparse.FileType('r', encoding='utf-8'), required=True)
    parser.add_argument('--output', type=argparse.FileType('w', encoding='utf-8'), required=True)
    args = parser.parse_args()

    books = json.load(args.input)
    for book in books:
        title = clean_title_for_search(book.get("title", "").strip())
        author = book.get("author", "").strip()
        q = urllib.parse.quote_plus(title)
        if author and author.lower() not in ["kindle edition", ""]:
            q += "+" + urllib.parse.quote_plus(author)
        book["amazon_search_url"] = f"https://www.amazon.com/s?k={q}"

    json.dump(books, args.output, indent=2, ensure_ascii=False)
    print(f"Added smart Amazon search URLs for {len(books)} books.")

if __name__ == "__main__":
    main()
