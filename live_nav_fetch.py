import requests
import pandas as pd
import os

os.makedirs("data/raw", exist_ok=True)

# Use actual codes from your fund_master
fund_master = pd.read_csv("data/raw/01_fund_master.csv")

# Pick 5 key schemes from your dataset
key_schemes = fund_master[
    fund_master['scheme_name'].str.contains('Bluechip|Large Cap', case=False, na=False)
].head(5)[['amfi_code', 'scheme_name']]

print("📋 Fetching these schemes:")
print(key_schemes.to_string(index=False))
print()

def fetch_nav(scheme_code, name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"⏳ Fetching {name} (code: {scheme_code})...")
    response = requests.get(url)
    data = response.json()

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

all_nav = []
for _, row in key_schemes.iterrows():
    df = fetch_nav(row['amfi_code'], row['scheme_name'])
    all_nav.append(df)

combined = pd.concat(all_nav, ignore_index=True)
combined.to_csv("data/raw/all_nav_combined.csv", index=False)
print(f"✅ Combined NAV saved → data/raw/all_nav_combined.csv")
print(f"   Total records: {len(combined)}")