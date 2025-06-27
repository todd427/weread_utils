# combine_kindle_books.py
import json
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Combine and deduplicate Kindle book JSON files.")
    parser.add_argument('--inputs', nargs='+', required=True, help="Input JSON files to combine")
    parser.add_argument('--output', required=True, help="Output deduplicated JSON file")
    args = parser.parse_args()

    seen = set()
    combined = []

    for input_file in args.inputs:
        with open(input_file, encoding='utf-8') as f:
            books = json.load(f)
        for book in books:
            # Use (title, author) as the deduplication key (case-insensitive, trimmed)
            title = book.get('title', '').strip().lower()
            author = book.get('author', '').strip().lower()
            key = (title, author)
            if key not in seen:
                combined.append(book)
                seen.add(key)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Combined and deduplicated {len(combined)} books into {args.output}")

if __name__ == "__main__":
    main()
