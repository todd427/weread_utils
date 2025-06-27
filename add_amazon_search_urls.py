# add_amazon_search_urls.py
import json
import argparse

def urlify_title(title):
    return '+'.join(title.split())

def main():
    parser = argparse.ArgumentParser(description="Add Amazon search URLs to every book entry.")
    parser.add_argument('--input', type=argparse.FileType('r', encoding='utf-8'), required=True)
    parser.add_argument('--output', type=argparse.FileType('w', encoding='utf-8'), required=True)
    args = parser.parse_args()

    books = json.load(args.input)
    for book in books:
        isbn = book.get("isbn", "")
        title = book.get("title", "")
        if isbn and len(isbn) >= 10:
            book["amazon_search_url"] = f"https://www.amazon.com/s?k={isbn}"
        elif title:
            book["amazon_search_url"] = f"https://www.amazon.com/s?k={urlify_title(title)}"
        else:
            book["amazon_search_url"] = ""
    json.dump(books, args.output, indent=2, ensure_ascii=False)
    print(f"Added Amazon search URLs for {len(books)} books.")

if __name__ == "__main__":
    main()
