import pandas as pd
from sqlalchemy import create_engine, text
import os

engine = create_engine("sqlite:///bluestock_mf.db")

# Run schema
with engine.connect() as conn:
    with open("schema.sql") as f:
        for stmt in f.read().split(";"):
            stmt = stmt.strip()
            if stmt:
                conn.execute(text(stmt))
    conn.commit()
print("✅ Schema created")

# ─── Load dim_fund ───────────────────────────────────────────────
df = pd.read_csv("data/processed/01_fund_master.csv")
df.to_sql("dim_fund", engine, if_exists="replace", index=False)
print(f"✅ dim_fund loaded ({len(df)} rows)")

# ─── Load fact_nav ───────────────────────────────────────────────
df = pd.read_csv("data/processed/nav_history_clean.csv")
df.to_sql("fact_nav", engine, if_exists="replace", index=False)
print(f"✅ fact_nav loaded ({len(df)} rows)")

# ─── Load fact_transactions ──────────────────────────────────────
df = pd.read_csv("data/processed/investor_transactions_clean.csv")
df.to_sql("fact_transactions", engine, if_exists="replace", index=False)
print(f"✅ fact_transactions loaded ({len(df)} rows)")

# ─── Load fact_performance ───────────────────────────────────────
df = pd.read_csv("data/processed/scheme_performance_clean.csv")
df.to_sql("fact_performance", engine, if_exists="replace", index=False)
print(f"✅ fact_performance loaded ({len(df)} rows)")

# ─── Load fact_aum ───────────────────────────────────────────────
df = pd.read_csv("data/processed/03_aum_by_fund_house.csv")
df.to_sql("fact_aum", engine, if_exists="replace", index=False)
print(f"✅ fact_aum loaded ({len(df)} rows)")

# ─── Verify row counts ───────────────────────────────────────────
print("\n📊 Verifying row counts:")
tables = ["dim_fund","fact_nav","fact_transactions","fact_performance","fact_aum"]
with engine.connect() as conn:
    for table in tables:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f"  {table}: {count} rows")

print("\n✅ Database loaded → bluestock_mf.db")