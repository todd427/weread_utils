#!/bin/bash

# Usage:
#   bash pipeline_wereader.sh --page toddReads/page3
#   OR
#   bash pipeline_wereader.sh --page /full/path/to/page3

# ---- ARGUMENT PARSING ----
if [[ $# -gt 0 ]]; then
  while [[ $# -gt 0 ]]; do
    case $1 in
      --page)
        PAGE="$2"
        shift
        shift
        ;;
      *)
        echo "[x] Unknown option: $1"
        exit 1
        ;;
    esac
  done
fi

if [ -z "$PAGE" ]; then
  echo "Usage: $0 --page path/to/html_file_without_ext"
  exit 1
fi

BASENAME=$(basename "$PAGE")
BASEDIR=$(dirname "$PAGE")
INPUT_HTML="${PAGE}.htm"

JSON="${BASEDIR}/${BASENAME}.json"
CLEAN_JSON="clean_${BASEDIR}/${BASENAME}_clean.json"
ENRICHED_JSON="enrich_${BASEDIR}/${BASENAME}_enriched.json"
AZT_JSON="AZT_${BASEDIR}/${BASENAME}_amazon_tagged.json"
FINAL_JSON="Aurls_${BASEDIR}/${BASENAME}_final.json"

mkdir -p "clean_${BASEDIR}" "enrich_${BASEDIR}" "AZT_${BASEDIR}" "Aurls_${BASEDIR}"

# ---- PIPELINE ----

echo "[1/5] Converting HTML to JSON..."
python kindle_to_json.py --input "$INPUT_HTML" --output "$JSON" || exit 1

echo "[2/5] Cleaning JSON..."
python clean_json.py --input "$JSON" --output "$CLEAN_JSON" || exit 1

echo "[3/5] Enriching via Google Books..."
python enrich_google_books.py --input "$CLEAN_JSON" --output "$ENRICHED_JSON" || exit 1

echo "[4/5] Extracting Amazon Title/Author..."
python amazon_title_author.py --input "$ENRICHED_JSON" --output "$AZT_JSON" || exit 1

echo "[5/5] Fetching Amazon URLs..."
python amazon_url.py --input "$AZT_JSON" --output "$FINAL_JSON" || exit 1

echo "[✓] Final output: $FINAL_JSON"
