import pandas as pd

fund_master = pd.read_csv("data/raw/01_fund_master.csv")
nav_history = pd.read_csv("data/raw/02_nav_history.csv")

master_codes = set(fund_master['amfi_code'])
nav_codes = set(nav_history['amfi_code'])

matched = master_codes & nav_codes
missing = master_codes - nav_codes

print("=" * 50)
print("AMFI CODE VALIDATION")
print("=" * 50)
print(f"✅ Total codes in fund_master : {len(master_codes)}")
print(f"✅ Codes matched in nav_history: {len(matched)}")
print(f"⚠️  Missing codes              : {len(missing)}")
if missing:
    print(f"   Missing: {missing}")

# Data quality summary
os.makedirs("reports", exist_ok=True)
with open("reports/data_quality_day1.txt", "w") as f:
    f.write("DATA QUALITY SUMMARY - DAY 1\n")
    f.write("=" * 40 + "\n")
    f.write(f"Total codes in fund_master : {len(master_codes)}\n")
    f.write(f"Matched in nav_history     : {len(matched)}\n")
    f.write(f"Missing codes              : {len(missing)}\n")
    if missing:
        f.write(f"Missing list               : {missing}\n")
    f.write("\nNOTE: 04_monthly_sip_inflows.csv has 12 null values in yoy_growth_pct (expected — first year has no YoY data)\n")

print("\n✅ Report saved → reports/data_quality_day1.txt")

import os