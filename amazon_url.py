# amazon_url.py
import json
import argparse
import urllib.parse

def isbn13_to_isbn10(isbn13):
    if not isbn13 or not isbn13.startswith("978") or len(isbn13) != 13:
        return None
    core = isbn13[3:-1]
    total = sum((10 - i) * int(num) for i, num in enumerate(core))
    check = 11 - (total % 11)
    if check == 10:
        check_char = "X"
    elif check == 11:
        check_char = "0"
    else:
        check_char = str(check)
    return core + check_char

def main():
    parser = argparse.ArgumentParser(description="Add best possible Amazon URLs to every book entry.")
    parser.add_argument('--input', type=argparse.FileType('r', encoding='utf-8'), required=True)
    parser.add_argument('--output', type=argparse.FileType('w', encoding='utf-8'), required=True)
    args = parser.parse_args()

    books = json.load(args.input)
    for book in books:
        asin = book.get("asin", "")
        isbn = book.get("isbn", "")
        isbn10 = ""
        if isbn and len(isbn) == 13:
            isbn10 = isbn13_to_isbn10(isbn)
        title = book.get("title", "")
        author = book.get("author", "")

        url = ""
        if asin and len(asin) == 10:
            url = f"https://www.amazon.com/dp/{asin}"
        elif isbn and len(isbn) == 10:
            url = f"https://www.amazon.com/dp/{isbn}"
        elif isbn10:
            url = f"https://www.amazon.com/dp/{isbn10}"
        elif title:
            q = urllib.parse.quote_plus(title)
            if author and author.lower() not in ["kindle edition", ""]:
                q += "+" + urllib.parse.quote_plus(author)
            url = f"https://www.amazon.com/s?k={q}"
        else:
            url = ""
        book["amazon_url"] = url

    json.dump(books, args.output, indent=2, ensure_ascii=False)
    print(f"Added best possible Amazon URLs for {len(books)} books.")

if __name__ == "__main__":
    main()
