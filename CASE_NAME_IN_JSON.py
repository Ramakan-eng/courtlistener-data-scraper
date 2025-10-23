# save as fetch_courtlistener_sample.py
import requests
import json
import sys
from time import sleep

# === Put your token here (you gave it above). Recommended: set this as an env var instead.
TOKEN = "643b57a151518628e9af48254933af9b24a93144"

# Base URL: choose endpoint you want. Here I use the opinions endpoint to get case opinions (small sample).
# BASE_URL = "https://www.courtlistener.com/api/rest/v3/opinions/"
BASE_URL = "https://www.courtlistener.com/api/rest/v4/search/"

# Small page size so we only get a sample
params = {
    "page_size": 5,        # small sample
    # optionally filter/order: e.g., "order_by": "-date_filed", "court": "scotus"
}

# two header variants commonly used (try one then fallback)
headers_try = [
    {"Authorization": f"Token {TOKEN}", "User-Agent": "sample-script/1.0 (youremail@example.com)"},
    {"Authentication": f"Token {TOKEN}", "User-Agent": "sample-script/1.0 (youremail@example.com)"},
]

def fetch_sample():
    last_exc = None
    for headers in headers_try:
        try:
            r = requests.get(BASE_URL, headers=headers, params=params, timeout=30)
            # if token invalid, API usually returns 401
            if r.status_code == 401:
                last_exc = Exception("401 Unauthorized with header: " + str(headers.keys()))
                # try next header style
                continue
            r.raise_for_status()
            data = r.json()
            # Save results field if present (v3/v4 may differ slightly)
            results = data.get("results") or data  # some endpoints return list directly
            filename = "courtlistener_sample.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(results) if hasattr(results, '__len__') else 'N/A'} items to {filename}")
            # print small preview (first item)
            if isinstance(results, list) and results:
                print("\nPreview of first item:")
                print(json.dumps(results[0], indent=2)[:1000])  # truncated preview
            return
        except requests.exceptions.RequestException as e:
            last_exc = e
            # small polite pause before next attempt
            sleep(0.5)

    # if we reach here, all header attempts failed
    print("Failed to fetch data. Last error:", last_exc, file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    fetch_sample()
