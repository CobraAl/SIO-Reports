import requests
from datetime import datetime, timedelta, timezone
import csv
import os
import pandas as pd
from dotenv import load_dotenv

# virtual environment setup
load_dotenv()
API_KEY = os.getenv("API_KEY")

# steps and logs
if not API_KEY:
    raise ValueError("API_KEY not found in .env file.")
print(f"🔐 API Key Loaded: {API_KEY[:5]}...")

# config
ENDPOINT = "https://app.standardinformation.io/api/reports"
BUYER_FILE = "BUYERS_ID.xlsx"
OUTPUT_FOLDER = "reports"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# date range
end_date = datetime.now(timezone.utc)
start_date = end_date - timedelta(days=30)
start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
today_str = end_date.strftime("%Y-%m-%d")

# Headers
headers = {
    "Authorization": API_KEY
}

# === LOAD BUYERS ===
buyers_df = pd.read_excel(BUYER_FILE)
buyers = buyers_df.to_dict(orient="records")
buyer_ids = [str(b['id']) for b in buyers]

# === API CALL ===
params = {
    "startDate": start_date_str,
    "endDate": end_date_str,
    "buyerIds": ",".join(buyer_ids)
}

print("🔄 Fetching data for all buyers in a single call...")

response = requests.get(ENDPOINT, headers=headers, params=params)

if response.status_code == 200:
    json_response = response.json()
    data = json_response.get("data", [])

    if isinstance(data, list) and data:
        keys = data[0].keys()
        filename = f"All_Buyers_{today_str}.csv"
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        with open(output_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

        print(f"✅ All data saved to {output_path}")
    else:
        print("⚠️ No data returned.")
else:
    print(f"❌ API error: {response.status_code}")
    print(response.text)
