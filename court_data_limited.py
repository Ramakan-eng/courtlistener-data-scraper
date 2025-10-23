import requests
import json

API_URL = "https://www.courtlistener.com/api/rest/v4/courts/"
LIMIT = 50  # total records to fetch

def fetch_courts(limit=LIMIT):
    url = API_URL
    courts = []
    total = 0

    print(f"Fetching up to {limit} court records...\n")

    while url and total < limit:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Request failed with {response.status_code}")
            break

        data = response.json()
        results = data.get("results", [])
        for court in results:
            courts.append({
                "id": court.get("id"),
                "name": court.get("name"),
                "full_name": court.get("full_name"),
                "jurisdiction": court.get("jurisdiction"),
                "url": court.get("url"),
            })
            total += 1
            print(f"{court['id']}: {court['full_name']} ({court['jurisdiction'][0].upper()})")

            if total >= limit:
                break

        url = data.get("next")

    # ✅ Save to JSON file
    with open("courts_data.json", "w", encoding="utf-8") as f:
        json.dump(courts, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved {len(courts)} courts to 'courts_data.json'")

if __name__ == "__main__":

    fetch_courts()
