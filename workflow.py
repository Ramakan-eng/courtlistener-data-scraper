import requests
import json
import sys

TOKEN = "643b57a151518628e9af48254933af9b24a93144"
BASE = "https://www.courtlistener.com/api/rest/v4/"

HEADERS = {"Authorization": f"Token {TOKEN}", "User-Agent": "courtlistener-client/1.0"}

def get_json(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    if r.status_code != 200:
        print(f"❌ Error {r.status_code}: {r.text}")
        sys.exit(1)
    return r.json()

# === Step 1: Search Case ===
case_name = "Tulsi Sawlani, M.D. v. Lake County Assessor"
search_url = BASE + "search/"
search_params = {"q": case_name, "page_size": 1}
search_data = get_json(search_url, search_params)

if not search_data.get("results"):
    print("❌ Case not found.")
    sys.exit(0)

case = search_data["results"][0]
cluster_id = case.get("cluster_id")
docket_id = case.get("docket_id")
court_id = case.get("court_id")

print(f"\n🔍 Found case: {case['caseName']}")
print(f"Cluster ID: {cluster_id}")
print(f"Docket ID: {docket_id}")
print(f"Court ID: {court_id}")

# === Step 2: Fetch Cluster Info ===
if cluster_id:
    cluster_data = get_json(BASE + f"clusters/{cluster_id}/")
    print("\n📦 Cluster Info:")
    print(json.dumps(cluster_data, indent=2)[:1000])

# === Step 3: Fetch Opinions ===
if cluster_id:
    opinions_data = get_json(BASE + "opinions/", {"cluster": cluster_id})
    print("\n📄 Opinions:")
    print(json.dumps(opinions_data["results"], indent=2)[:1000])

# === Step 4: Fetch Docket Info ===
if docket_id:
    docket_data = get_json(BASE + f"dockets/{docket_id}/")
    print("\n📁 Docket Info:")
    print(json.dumps(docket_data, indent=2)[:1000])

# === Step 5: Fetch Court Info ===
if court_id:
    court_data = get_json(BASE + f"courts/{court_id}/")
    print("\n⚖️ Court Info:")
    print(json.dumps(court_data, indent=2)[:1000])


result = {
    "search": case,
    "cluster": cluster_data,
    "opinions": opinions_data.get("results", []),
    "docket": docket_data,
    "court": court_data,
}

with open("Tulsi_Sawlani_case.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("\n✅ All data saved to Tulsi_Sawlani_case.json")

