import requests
import json

API_TOKEN = "643b57a151518628e9af48254933af9b24a93144"  # <-- replace with your real API token
HEADERS = {"Authorization": f"Token {API_TOKEN}"}

def fetch_courts():
    url = "https://www.courtlistener.com/api/rest/v4/courts/"
    courts = []

    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ Failed to fetch courts: {response.status_code}")
            break

        data = response.json()
        results = data.get("results", [])
        if not results:
            print("⚠️ No results found on this page.")
            break

        for court in results:
            # Use .get() to avoid KeyError
            courts.append({
                "id": court.get("id"),
                  "name": court.get("name", "N/A"),
                "slug": court.get("slug", "N/A"),
                "abbreviation": court.get("abbreviation", "N/A"),
                "jurisdiction": court.get("jurisdiction", "N/A"),
                "url": court.get("url", "N/A")
            })

        for court in data["results"]:
            print(f"{court.get('id')}: {court.get('full_name')} ({court.get('jurisdiction')})")
            print(f"✅ Page processed, total courts so far: {len(courts)}\n")
 

    # Save results
    with open("courts_data.json", "w", encoding="utf-8") as f:
        json.dump(courts, f, indent=2, ensure_ascii=False)

    print(f"✅ Extracted {len(courts)} courts and saved to courts_data.json")

if __name__ == "__main__":
    fetch_courts()
