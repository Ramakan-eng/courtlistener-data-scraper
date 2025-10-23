import requests
import json
import time

# === Your CourtListener API token ===
TOKEN = "643b57a151518628e9af48254933af9b24a93144"
BASE_URL = "https://www.courtlistener.com/api/rest/v4/"
HEADERS = {"Authorization": f"Token {TOKEN}", "User-Agent": "courtlistener-client/1.0"}

# === Helper: Safe API request ===
def get_json(url, params=None):
    """Safely fetch JSON from API with retries."""
    for _ in range(3):
        r = requests.get(url, headers=HEADERS, params=params)
        if r.status_code == 200:
            return r.json()
        elif r.status_code in [429, 503]:
            time.sleep(1.5)  # rate limit handling
        else:
            print(f"⚠️ Error {r.status_code} for {url}")
            return {}
    return {}

# === Step 1: Search Cases ===
def search_cases(query, page_size=5):
    url = BASE_URL + "search/"
    params = {"q": query, "page_size": page_size}
    data = get_json(url, params)
    return data.get("results", [])

# === Step 2: Fetch cluster, opinions, docket, court info for each case ===
def fetch_case_details(case):
    cluster_id = case.get("cluster_id")
    docket_id = case.get("docket_id")
    court_id = case.get("court_id")

    details = {"search_result": case}

    # Cluster
    if cluster_id:
        cluster = get_json(BASE_URL + f"clusters/{cluster_id}/")
        details["cluster"] = cluster
        time.sleep(0.2)

    # Opinions
    if cluster_id:
        opinions = get_json(BASE_URL + "opinions/", {"cluster": cluster_id})
        details["opinions"] = opinions.get("results", [])
        time.sleep(0.2)

    # Docket
    if docket_id:
        docket = get_json(BASE_URL + f"dockets/{docket_id}/")
        details["docket"] = docket
        time.sleep(0.2)

    # Court
    if court_id:
        court = get_json(BASE_URL + f"courts/{court_id}/")
        details["court"] = court
        time.sleep(0.2)

    return details

# === Step 3: Main flow ===
def main():
    query = input("Enter case search keyword: ").strip()
    results = search_cases(query, page_size=10)

    if not results:
        print("❌ No results found.")
        return

    print(f"✅ Found {len(results)} cases. Fetching detailed info...")

    all_cases_data = []
    for i, case in enumerate(results, start=1):
        print(f"\n🔹 Processing case {i}/{len(results)}: {case.get('caseName')}")
        case_details = fetch_case_details(case)
        all_cases_data.append(case_details)

    # === Save all cases in one JSON ===
    with open("courtlistener_all_cases.json", "w", encoding="utf-8") as f:
        json.dump(all_cases_data, f, indent=2, ensure_ascii=False)

    print("\n✅ All case data saved to 'courtlistener_all_cases.json'")

if __name__ == "__main__":
    main()
