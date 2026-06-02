import requests
import pandas as pd
import os

os.makedirs("data/raw", exist_ok=True)

schemes = {
    119551: "SBI Bluechip",
    120503: "ICICI Bluechip",
    118632: "Nippon Large Cap",
    119092: "Axis Bluechip",
    120841: "Kotak Bluechip",
}

def fetch_nav(scheme_code, name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"⏳ Fetching {name} (code: {scheme_code})...")
    response = requests.get(url)
    data = response.json()

    meta = data.get('meta', {})
    print(f"   Fund: {meta.get('fund_house', 'N/A')}")
    print(f"   Scheme: {meta.get('scheme_name', 'N/A')}")

    nav_df = pd.DataFrame(data['data'])
    nav_df['scheme_code'] = scheme_code
    nav_df['scheme_name'] = name

    filename = f"data/raw/nav_{scheme_code}_{name.replace(' ', '_')}.csv"
    nav_df.to_csv(filename, index=False)
    print(f"   ✅ Saved → {filename} ({len(nav_df)} records)")
    return nav_df

all_nav = []
for code, name in schemes.items():
    df = fetch_nav(code, name)
    all_nav.append(df)

combined = pd.concat(all_nav, ignore_index=True)
combined.to_csv("data/raw/all_nav_combined.csv", index=False)
print(f"\n✅ Combined NAV saved → data/raw/all_nav_combined.csv")
print(f"   Total records: {len(combined)}")