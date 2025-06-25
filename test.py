import requests
from datetime import datetime, timedelta, timezone
import csv
import os
import time

# === CONFIGURATION ===
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
ENDPOINT = "https://app.standardinformation.io/api/reports"
OUTPUT_FOLDER = "reports"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === DATE RANGE: Last 30 days ===
end_date = datetime.now(timezone.utc)
start_date = end_date - timedelta(days=30)
start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
today_str = end_date.strftime("%Y-%m-%d")

# === BUYER INFO (edit these) ===
buyer_id = "1000679"            # ID of the buyer
buyer_name = "Go Gamma"         # Name of the buyer
buyer_name_clean = buyer_name.strip().replace("/", "-")

# === HEADERS ===
headers = {
    "Authorization": API_KEY
}

# === API REQUEST ===
print(f"Fetching data for buyer {buyer_name} ({buyer_id})...")

params = {
    "startDate": start_date_str,
    "endDate": end_date_str,
    "buyerId": buyer_id
}

response = requests.get(ENDPOINT, headers=headers, params=params)

if response.status_code == 429:
    print(f"Rate limit reached. Waiting 10 seconds before retrying...")
    time.sleep(10)
    response = requests.get(ENDPOINT, headers=headers, params=params)

if response.status_code == 200:
    json_response = response.json()
    data = json_response.get("data", [])

    if isinstance(data, list) and data:
        keys = data[0].keys()
        filename = f"{buyer_name_clean}_{today_str}.csv"
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        with open(output_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

        print(f"Data saved to {output_path}")
    else:
        print(f"No data found for {buyer_name}")
else:
    print(f"API error {response.status_code} for {buyer_name}")
    print(response.text)
