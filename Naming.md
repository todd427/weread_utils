Perfect — we'll make just one tweak for clarity and finality:

* Change **`page3_with_urls.json`** → **`page3_final.json`**

Here’s the updated mapping:

| Phase               | Directory           | Filename                   |
| ------------------- | ------------------- | -------------------------- |
| Raw Kindle HTML     | `toddReads/`        | `page3.json`               |
| Cleaned JSON        | `clean_toddReads/`  | `page3_clean.json`         |
| Enriched via Google | `enrich_toddReads/` | `page3_enriched.json`      |
| Amazon Title/Author | `AZT_toddReads/`    | `page3_amazon_tagged.json` |
| Final Output        | `Aurls_toddReads/`  | `page3_final.json`         |

---

### ✅ Updated `pipeline_wereader.sh` variable block:

```bash
BASENAME=$(basename "$PAGE")
JSON="$PAGE.json"
CLEAN_JSON="clean_${BASENAME}_clean.json"
ENRICHED_JSON="enrich_${BASENAME}_enriched.json"
AZT_JSON="AZT_${BASENAME}_amazon_tagged.json"
FINAL_JSON="Aurls_${BASENAME}_final.json"
```

Would you like me to generate and send the full updated `pipeline_wereader.sh` now?
