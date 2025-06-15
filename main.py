import requests
from datetime import datetime, timedelta, timezone
import csv
import os
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

# === CONFIG ===
API_KEY = os.getenv("API_KEY")
ENDPOINT = "https://app.standardinformation.io/api/reports"
BUYER_FILE = "BUYERS_ID.xlsx"
OUTPUT_FOLDER = "reports"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === DATE RANGE: Last 30 days ===
end_date = datetime.now(timezone.utc)
start_date = end_date - timedelta(days=30)
start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
today_str = end_date.strftime("%Y-%m-%d")

# === HEADERS ===
headers = {
    "Authorization": API_KEY
}

# === LOAD BUYERS ===
buyers_df = pd.read_excel(BUYER_FILE)
buyers = buyers_df.to_dict(orient="records")

# === LOOP THROUGH BUYERS ===
for buyer in buyers:
    buyer_id = str(buyer['id'])
    buyer_name = buyer['Buyer'].strip().replace("/", "-")  # avoid invalid filename chars

    print(f"🔄 Fetching data for buyer {buyer_name} ({buyer_id})...")

    params = {
        "startDate": start_date_str,
        "endDate": end_date_str,
        "buyerId": buyer_id
    }

    response = requests.get(ENDPOINT, headers=headers, params=params)

    if response.status_code == 200:
        json_response = response.json()
        data = json_response.get("data", [])

        if isinstance(data, list) and data:
            keys = data[0].keys()
            filename = f"{buyer_name}_{today_str}.csv"
            output_path = os.path.join(OUTPUT_FOLDER, filename)

            with open(output_path, "w", newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)

            print(f"✅ Data saved to {output_path}")
        else:
            print(f"⚠️ No data for {buyer_name}")
    else:
        print(f"❌ API error for {buyer_name}: {response.status_code}")
        print(response.text)
