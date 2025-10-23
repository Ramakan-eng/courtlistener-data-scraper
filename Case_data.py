import requests

API_TOKEN = "643b57a151518628e9af48254933af9b24a93144"
HEADERS = {"Authorization": f"Token {API_TOKEN}"}

def fetch_case_details(case_name):
    # 1️⃣ Search case from opinions
    opinions_url = "https://www.courtlistener.com/api/rest/v4/opinions/"
    params = {"search": case_name, "page_size": 1}
    response = requests.get(opinions_url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"API request failed ({response.status_code})")
        return

    data = response.json()
    results = data.get("results", [])
    if not results:
        print("No results found for this case.")
        return

    case = results[0]
    cluster_url = case.get("cluster")

    # 2️⃣ Get cluster info for metadata
    case_name_out, court_name, date_filed = None, None, None
    if cluster_url:
        cluster_resp = requests.get(cluster_url, headers=HEADERS)
        if cluster_resp.status_code == 200:
            cluster_data = cluster_resp.json()
            case_name_out = cluster_data.get("case_name")
            court_name = cluster_data.get("court")
            date_filed = cluster_data.get("date_filed")

    # 3️⃣ Extract opinion text (check multiple fields)
    opinion_text = (
        case.get("plain_text")
        or case.get("html_lawbox")
        or case.get("html_columbia")
        or case.get("html_with_citations")
    )

    print("\n📄 Case Details:")
    print("Case Name:", case_name_out or case.get("case_name"))
    print("Court:", court_name or case.get("court"))
    print("Filed Date:", date_filed or case.get("date_filed"))
    print("Cluster URL:", cluster_url)
    print("Opinion URL:", case.get("absolute_url"))

    if opinion_text:
        # Remove HTML tags for readability (optional)
        import re
        clean_text = re.sub(r"<[^>]+>", "", opinion_text)
        print("\n🧾 Opinion Text (first 500 chars):\n")
        print(clean_text[:500])
    else:
        print("\n Opinion text not available in any format.")

if __name__ == "__main__":
    case_name = input("Enter case name: ")
    fetch_case_details(case_name)
