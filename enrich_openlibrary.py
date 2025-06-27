# enrich_openlibrary.py
import json
import argparse
import requests
import time
import sys

def get_google_books_info(title):
    print(f"Searching Google Books for: {title}")
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": title}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if "items" in data:
            book = data["items"][0]["volumeInfo"]
            isbn = ""
            for identifier in book.get("industryIdentifiers", []):
                if identifier["type"] in ["ISBN_13", "ISBN_10"]:
                    isbn = identifier["identifier"]
                    break
            info_url = book.get("infoLink", "")
            return isbn, info_url
    except Exception as e:
        print(f"Error searching {title}: {e}", file=sys.stderr)
    return "", ""

def get_open_library_info(title):
    url = "https://openlibrary.org/search.json"
    params = {"title": title}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("docs"):
            doc = data["docs"][0]
            isbn = doc.get("isbn", [""])[0] if doc.get("isbn") else ""
            olid = doc.get("key", "")
            return isbn, f"https://openlibrary.org{olid}" if olid else ""
    except Exception as e:
        print(f"Error searching {title}: {e}", file=sys.stderr)
    return "", ""

def main():
    parser = argparse.ArgumentParser(description="Enrich books with ISBN and Open Library URL using Open Library API.")
    parser.add_argument("--input", type=argparse.FileType("r", encoding="utf-8"), default=sys.stdin, help="Input JSON file (default: stdin)")
    parser.add_argument("--output", type=argparse.FileType("w", encoding="utf-8"), default=sys.stdout, help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    books = json.load(args.input)
    for book in books:
        print(f"Enriching: {book.get('title', '')}")
        isbn, ol_url = get_google_books_info(book["title"])
        book["isbn"] = isbn
        book["openlibrary_url"] = ol_url
        print(f"-> ISBN: {isbn}, OL: {ol_url}")
        time.sleep(1)  # Be gentle to the API!

    json.dump(books, args.output, indent=2, ensure_ascii=False)
    print(f"\nEnriched {len(books)} books. Results saved.", file=sys.stderr)

if __name__ == "__main__":
    main()
