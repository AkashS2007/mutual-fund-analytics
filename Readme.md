# Capstone Project I — Mutual Fund Analytics
**Bluestock Fintech | Batch MJ28**

## Project Overview
A complete end-to-end mutual fund analytics platform built on 10 AMFI datasets covering 40 schemes, 32,778 investor transactions, and 64,320 NAV records spanning 2022–2026.

## Team Members
- akashs3882, bandarivyshnavi2, vhedau47, Kota Naga Raviteja, divyamadiraju2006

## Project Structure
mutual-fund-analytics/

├── data/

│   ├── raw/              # Original 10 CSV datasets

│   └── processed/        # Cleaned datasets + DB

├── notebooks/            # Jupyter analysis notebooks

├── dashboard/            # Power BI files

├── reports/              # PDF report + charts

├── sql/                  # Schema + queries

└── scripts/
## Setup Instructions
```bash
# Clone the repo
git clone https://github.com/AkashS2007/mutual-fund-analytics.git
cd mutual-fund-analytics

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

## How to Run the ETL Pipeline
```bash
python run_pipeline.py
```
This runs: data ingestion → cleaning → database load → analytics

## How to Open the Dashboard
1. Open Power BI Desktop
2. File → Open → `dashboard/bluestock_mf_dashboard.pbix`

## Dataset Descriptions
| File | Description | Rows |
|------|-------------|------|
| 01_fund_master.csv | 40 mutual fund schemes with metadata | 40 |
| 02_nav_history.csv | Daily NAV from 2022–2026 | 46,000 |
| 03_aum_by_fund_house.csv | Quarterly AUM by AMC | 90 |
| 04_monthly_sip_inflows.csv | Monthly SIP flow data | 48 |
| 05_category_inflows.csv | Category-wise net inflows | 144 |
| 06_industry_folio_count.csv | Total industry folios | 21 |
| 07_scheme_performance.csv | Risk/return metrics | 40 |
| 08_investor_transactions.csv | 32K investor transactions | 32,778 |
| 09_portfolio_holdings.csv | Sector/stock holdings | 322 |
| 10_benchmark_indices.csv | Nifty 50/100 daily data | 8,050 |

## Key Findings
1. SBI Mutual Fund dominates AUM at ₹12.5L Cr
2. SIP inflows hit all-time high of ₹31,002 Cr in Dec 2025
3. Total folios doubled from 13.26 Cr to 26.12 Cr in 4 years
4. Small Cap funds outperform Large Cap by 8–12% over 3 years
5. 18% of SIP investors flagged as at-risk (gap > 35 days)