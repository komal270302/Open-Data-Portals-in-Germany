import requests

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Get all group IDs
group_list_url = "https://www.daten-bw.de/ckan/api/3/action/group_list"
group_ids = requests.get(group_list_url, headers=headers, timeout=15).json()["result"]

print("Categories:\n")

# Loop through each group and print name + dataset count
for group_id in group_ids:
    group_show_url = f"https://www.daten-bw.de/ckan/api/3/action/group_show?id={group_id}"
    group_data = requests.get(group_show_url, headers=headers, timeout=15).json()["result"]
    title_en = group_data.get("title_translated", {}).get("en", group_data.get("display_name", group_id))

    search_url = f"https://www.daten-bw.de/ckan/api/3/action/package_search?q=groups:{group_id}"
    response = requests.get(search_url, headers=headers, timeout=15).json()
    count = response["result"]["count"]
    if count > 0:
        print(f"{title_en} ({count})")


