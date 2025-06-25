# StandardInfo Data Fetcher

This Python script fetches 30-day lead data for multiple buyers from the StandardInformation API and saves a separate CSV file for each buyer.

## Features
- Loops through buyer list from an Excel file
- Pulls clean data from API using secure API key from `.env`
- Automatically names files with buyer name and date
- Organized output into `/reports` folder

## Usage

1. Install requirements:
2. Create `.env` with: API_KEY=your_api_key_here
3. Run the script: python main.py


## Output

One CSV file per buyer in the `reports/` folder, e.g.:
