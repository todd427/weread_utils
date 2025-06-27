#!/bin/bash

set -e

# --- USAGE ---
usage() {
    echo "Usage: $0 --page <file path without .htm>"
    echo "Example: $0 --page toddReads/page2"
    exit 1
}

# --- ARG PARSE ---
if [[ $# -gt 0 ]]; then
    case $1 in
        --page) PAGE="$2"; shift 2 ;;
        *) usage ;;
    esac
fi

[[ -z "$PAGE" ]] && usage

# --- DYNAMIC PATHS ---
DIR=$(dirname "$PAGE")
BASE=$(basename "$PAGE")
INPUT_HTML="${PAGE}.htm"

JSON="${DIR}/${BASE}.json"
CLEAN_JSON="clean_${DIR}/${BASE}.json"
ENRICHED_JSON="enrich_${DIR}/${BASE}.json"
AZT_JSON="AZT_${DIR}/${BASE}.json"
FINAL_JSON="Aurls_${DIR}/${BASE}.json"

mkdir -p "$(dirname "$CLEAN_JSON")" "$(dirname "$ENRICHED_JSON")" "$(dirname "$AZT_JSON")" "$(dirname "$FINAL_JSON")"

# --- RUN PIPELINE ---
echo "[1/5] Converting HTML to JSON..."
python kindle_to_json.py --input "$INPUT_HTML" --output "$JSON"

echo "[2/5] Cleaning JSON..."
python clean_json.py --input "$JSON" --output "$CLEAN_JSON"

echo "[3/5] Enriching via Google Books..."
python enrich_google_books.py --input "$CLEAN_JSON" --output "$ENRICHED_JSON"

echo "[4/5] Extracting Amazon Title/Author..."
python amazon_title_author.py --input "$ENRICHED_JSON" --output "$AZT_JSON"

echo "[5/5] Fetching Amazon URLs..."
python amazon_url.py --input "$AZT_JSON" --output "$FINAL_JSON"

echo "[✓] Final output: $FINAL_JSON"
