# clean_json.py
import json
import argparse

JUNK_KEYWORDS = [
    "your account", "not yet shipped", "amazon pay", "click here",
    "report the bug", "product safety", "recalls", "returns", "sign in",
    "see what's new", "your orders"
]


def is_valid_book(entry):
    title = entry.get("title", "").strip().lower()
    if not title or len(title) < 10:
        return False
    if any(bad in title for bad in JUNK_KEYWORDS):
        return False
    return True

def clean_json(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    clean_data = []
    seen_titles = set()

    for entry in data:
        if not is_valid_book(entry):
            continue
        title = entry["title"].strip()
        if title in seen_titles:
            continue
        seen_titles.add(title)
        clean_data.append(entry)

    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(clean_data, outfile, indent=2)
    print(f"✅ Cleaned {len(clean_data)} entries written to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Raw JSON from html2json")
    parser.add_argument("--output", required=True, help="Cleaned JSON output")
    args = parser.parse_args()
    clean_json(args.input, args.output)
