import requests
import json
import time

TOKEN = "643b57a151518628e9af48254933af9b24a93144"
BASE_URL = "https://www.courtlistener.com/api/rest/v4/"
HEADERS = {"Authorization": f"Token {TOKEN}", "User-Agent": "courtlistener-client/1.0"}

# --- Helper for safe GET requests ---
def get_json(url, params=None):
    for _ in range(3):
        r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        if r.status_code == 200:
            return r.json()
        elif r.status_code in [429, 503]:
            time.sleep(1.5)
        else:
            print(f"⚠️ Error {r.status_code} for {url}")
            return {}
    return {}

# --- Step 1: Automatically fetch latest cases ---
def get_latest_cases(limit=10):
    url = BASE_URL + "search/"
    params = {"page_size": limit}  # get latest cases automatically
    data = get_json(url, params)
    return data.get("results", [])

# --- Step 2: Fetch related info for each case ---
def fetch_case_details(case):
    cluster_id = case.get("cluster_id")
    docket_id = case.get("docket_id")
    court_id = case.get("court_id")

    details = {"search_result": case}

    if cluster_id:
        details["cluster"] = get_json(BASE_URL + f"clusters/{cluster_id}/")
        print("   🔹 Cluster data fetched")
        time.sleep(0.3)
    if cluster_id:
        opinions = get_json(BASE_URL + "opinions/", {"cluster": cluster_id})
        details["opinions"] = opinions.get("results", [])
        print("   🔹 Opinions fetched")
        time.sleep(0.3)
    if docket_id:
        details["docket"] = get_json(BASE_URL + f"dockets/{docket_id}/")
        print("   🔹 Docket data fetched")
        time.sleep(0.3)
    if court_id:
        details["court"] = get_json(BASE_URL + f"courts/{court_id}/")
        print("   🔹 Court info fetched")
        time.sleep(0.3)

    return details

# --- Step 3: Full workflow ---
def main():
    print("🔍 Fetching latest cases from CourtListener...")
    latest_cases = get_latest_cases(limit=10)

    if not latest_cases:
        print("❌ No cases found.")
        return

    print(f"✅ Found {len(latest_cases)} latest cases. Gathering details...\n")

    all_data = []

    for i, case in enumerate(latest_cases, start=1):
        case_name = case.get("caseName", "Unnamed Case")
        print(f"⚖️ [{i}/{len(latest_cases)}] Processing: {case_name}")
        details = fetch_case_details(case)
        all_data.append(details)

    # --- Save all data to JSON ---
    with open("courtlistener_latest_cases.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print("\n✅ All data saved to 'courtlistener_latest_cases.json'")

if __name__ == "__main__":
    main()
