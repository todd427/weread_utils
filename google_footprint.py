import argparse
import requests

def bing_search_count(query: str, api_key: str) -> int:
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    
    return data.get("webPages", {}).get("totalEstimatedMatches", 0)

def main():
    parser = argparse.ArgumentParser(description="Estimate Google/Bing web footprint for a given name or brand")
    parser.add_argument("query", help="Name, phrase, or company to search for")
    parser.add_argument("--api-key", required=True, help="Your Bing Search v7 API key")

    args = parser.parse_args()
    
    try:
        count = bing_search_count(args.query, args.api_key)
        print(f"\n🔍 '{args.query}' → Estimated matches: {count:,}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
