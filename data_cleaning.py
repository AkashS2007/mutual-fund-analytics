import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)

# ─── 1. Clean nav_history ───────────────────────────────────────
print("🧹 Cleaning 02_nav_history.csv...")
nav = pd.read_csv("data/raw/02_nav_history.csv")

nav['date'] = pd.to_datetime(nav['date'])
nav = nav.sort_values(['amfi_code', 'date'])
nav = nav.drop_duplicates()
nav = nav[nav['nav'] > 0]
nav = nav.sort_values(['amfi_code', 'date']).reset_index(drop=True)

# Forward-fill missing NAV for holidays/weekends
nav = nav.set_index('date').groupby('amfi_code').resample('D').ffill().drop(columns='amfi_code').reset_index()

nav.to_csv("data/processed/nav_history_clean.csv", index=False)
print(f"  ✅ Saved → data/processed/nav_history_clean.csv ({len(nav)} rows)")

# ─── 2. Clean investor_transactions ─────────────────────────────
print("\n🧹 Cleaning 08_investor_transactions.csv...")
txn = pd.read_csv("data/raw/08_investor_transactions.csv")

txn['transaction_type'] = txn['transaction_type'].str.strip().str.title()
txn['transaction_type'] = txn['transaction_type'].replace({
    'Sip': 'SIP', 'Lumpsum': 'Lumpsum', 'Redemption': 'Redemption'
})
txn = txn[txn['amount_inr'] > 0]
txn['transaction_date'] = pd.to_datetime(txn['transaction_date'])
valid_kyc = ['Verified', 'Pending', 'Rejected']
txn = txn[txn['kyc_status'].isin(valid_kyc)]

txn.to_csv("data/processed/investor_transactions_clean.csv", index=False)
print(f"  ✅ Saved → data/processed/investor_transactions_clean.csv ({len(txn)} rows)")

# ─── 3. Clean scheme_performance ────────────────────────────────
print("\n🧹 Cleaning 07_scheme_performance.csv...")
perf = pd.read_csv("data/raw/07_scheme_performance.csv")

numeric_cols = ['return_1yr_pct','return_3yr_pct','return_5yr_pct',
                'benchmark_3yr_pct','alpha','beta','sharpe_ratio',
                'sortino_ratio','std_dev_ann_pct','max_drawdown_pct','expense_ratio_pct']

for col in numeric_cols:
    perf[col] = pd.to_numeric(perf[col], errors='coerce')

# Flag anomalies
anomalies = perf[(perf['expense_ratio_pct'] < 0.1) | (perf['expense_ratio_pct'] > 2.5)]
if len(anomalies) > 0:
    print(f"  ⚠️  Expense ratio anomalies: {len(anomalies)} rows")
    print(anomalies[['scheme_name','expense_ratio_pct']])
else:
    print("  ✅ Expense ratio all within 0.1–2.5% range")

perf.to_csv("data/processed/scheme_performance_clean.csv", index=False)
print(f"  ✅ Saved → data/processed/scheme_performance_clean.csv ({len(perf)} rows)")

# ─── Copy remaining CSVs to processed ───────────────────────────
other_files = [
    "01_fund_master.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

print("\n📋 Copying remaining CSVs to processed...")
for f in other_files:
    df = pd.read_csv(f"data/raw/{f}")
    df.to_csv(f"data/processed/{f}", index=False)
    print(f"  ✅ {f} ({len(df)} rows)")

print("\n✅ All data cleaning complete!")