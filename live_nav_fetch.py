import pandas as pd
import os
import requests
import time
from datetime import datetime

os.makedirs("data/raw", exist_ok=True)

# Check if fund_master exists
if not os.path.exists("data/raw/01_fund_master.csv"):
    print("❌ Error: data/raw/01_fund_master.csv not found")
    exit(1)

fund_master = pd.read_csv("data/raw/01_fund_master.csv")

# Pick 5 key schemes from your dataset
key_schemes = fund_master[
    fund_master['scheme_name'].str.contains('Bluechip|Large Cap', case=False, na=False)
].head(5)[['amfi_code', 'scheme_name']]

if key_schemes.empty:
    print("❌ No schemes found matching 'Bluechip|Large Cap'")
    exit(1)

print("📋 Fetching these schemes:")
print(key_schemes.to_string(index=False))
print()

def fetch_nav(scheme_code, name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"⏳ Fetching {name} (code: {scheme_code})...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Validate API response
        if 'data' not in data or not data['data']:
            print(f"   ⚠️  No data returned for this scheme\n")
            return None

        meta = data.get('meta', {})
        print(f"   Fund   : {meta.get('fund_house', 'N/A')}")
        print(f"   Scheme : {meta.get('scheme_name', 'N/A')}")

        nav_df = pd.DataFrame(data['data'])
        nav_df['scheme_code'] = scheme_code
        nav_df['scheme_name'] = name

        filename = f"data/raw/nav_{scheme_code}.csv"
        nav_df.to_csv(filename, index=False)
        print(f"   ✅ Saved → {filename} ({len(nav_df)} records)\n")
        
        return nav_df
    
    except requests.RequestException as e:
        print(f"   ❌ Error fetching data: {e}\n")
        return None

all_nav = []
for idx, (_, row) in enumerate(key_schemes.iterrows()):
    df = fetch_nav(row['amfi_code'], row['scheme_name'])
    if df is not None:
        all_nav.append(df)
    
    # Rate limiting - wait between requests
    if idx < len(key_schemes) - 1:
        time.sleep(1)

if all_nav:
    combined = pd.concat(all_nav, ignore_index=True)
    combined.to_csv("data/raw/all_nav_combined.csv", index=False)
    print(f"✅ Combined NAV saved → data/raw/all_nav_combined.csv")
    print(f"   Total records: {len(combined)}")
else:
    print("⚠️  No data was successfully fetched")