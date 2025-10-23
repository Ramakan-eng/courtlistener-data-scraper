import requests

API_TOKEN = "643b57a151518628e9af48254933af9b24a93144"  # ← paste your API key here
BASE_URL = "https://www.courtlistener.com/api/rest/v4/search/"

def get_case_details(case_name):
    print(f"Searching for '{case_name}' ...")

    headers = {
        "Authorization": f"Token {API_TOKEN}"
    }
    params = {
        "q": case_name,
        "type": "o",  # 'o' means opinions
        "page_size": 3,
        "format": "json"
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"API request failed ({response.status_code})")
        print(response.text)
        return

    data = response.json()
    results = data.get("results", [])
    if not results:
        print("⚠️ No results found.")
        return

    print(f"✅ Found {len(results)} results.")
    for i, case in enumerate(results[:3], 1):
        print(f"\n📄 Case {i}: {case.get('caseName', 'N/A')}")
        print(f"🏛️ Court: {case.get('court', 'N/A')}")
        print(f"📅 Date: {case.get('dateFiled', 'N/A')}")
        print(f"🔗 URL: {case.get('absolute_url', 'N/A')}")


if __name__ == "__main__":
    case_name = input("Enter case name: ")
    get_case_details(case_name)


