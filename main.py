import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
import pandas as pd
import os
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Constants
ENDPOINT = "https://app.standardinformation.io/api/reports"
BUYER_FILE = "BUYERS_ID.xlsx"

# Streamlit App
st.set_page_config(page_title="Download Sold Leads", layout="centered")
st.title("📥 Download Sold Leads (Past 30 Days)")

if not API_KEY:
    st.error("API_KEY not found in .env file. Please check your environment setup.")
else:
    if st.button("Download Report"):
        with st.spinner("Fetching data..."):

            try:
                # Date range
                end_date = datetime.now(timezone.utc)
                start_date = end_date - timedelta(days=30)
                start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

                # Load buyer IDs
                buyers_df = pd.read_excel(BUYER_FILE)
                buyer_ids = [str(b['id']) for b in buyers_df.to_dict(orient="records")]

                # API request
                params = {
                    "startDate": start_date_str,
                    "endDate": end_date_str,
                    "buyerIds": ",".join(buyer_ids)
                }
                headers = {"Authorization": API_KEY}

                response = requests.get(ENDPOINT, headers=headers, params=params)

                if response.status_code == 200:
                    json_response = response.json()
                    data = json_response.get("data", [])

                    if isinstance(data, list) and data:
                        df = pd.DataFrame(data)
                        csv_buffer = BytesIO()
                        df.to_csv(csv_buffer, index=False)
                        csv_buffer.seek(0)

                        today_str = end_date.strftime("%Y-%m-%d")
                        st.success("✅ Data fetched successfully!")
                        st.download_button(
                            label="📥 Click to Download CSV",
                            data=csv_buffer,
                            file_name=f"All_Buyers_{today_str}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("⚠️ No data returned from API.")
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error("An error occurred while fetching the report.")
                st.exception(e)
