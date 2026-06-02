import pandas as pd
import os

csv_files = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

for file in csv_files:
    path = os.path.join("data", "raw", file)
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"\n📄 {file}")
        print("  Shape     :", df.shape)
        print("  Dtypes    :\n", df.dtypes)
        print("  Head      :\n", df.head())
        # Note any anomalies
        nulls = df.isnull().sum().sum()
        if nulls > 0:
            print(f"  ⚠️  Null values found: {nulls}")
        else:
            print("  ✅ No null values")
    else:
        print(f"⚠️  File not found: {path}")

print("\n✅ Data ingestion exploration complete.")