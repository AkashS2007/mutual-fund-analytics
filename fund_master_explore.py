import pandas as pd

df = pd.read_csv("data/raw/01_fund_master.csv")

print("=" * 50)
print("FUND MASTER EXPLORATION")
print("=" * 50)

print(f"\n🏦 Unique Fund Houses ({df['fund_house'].nunique()}):")
print(df['fund_house'].unique())

print(f"\n📂 Categories ({df['category'].nunique()}):")
print(df['category'].unique())

print(f"\n📁 Sub-categories ({df['sub_category'].nunique()}):")
print(df['sub_category'].unique())

print(f"\n⚠️  Risk Grades ({df['risk_category'].nunique()}):")
print(df['risk_category'].unique())

print(f"\n🏷️  SEBI Category Codes ({df['sebi_category_code'].nunique()}):")
print(df['sebi_category_code'].unique())

print("\n✅ Fund Master exploration complete.")