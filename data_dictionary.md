# Data Dictionary — Bluestock Mutual Fund Analytics

## 1. dim_fund (01_fund_master.csv)
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | INTEGER | Unique AMFI scheme code (Primary Key) |
| fund_house | TEXT | Name of the Asset Management Company |
| scheme_name | TEXT | Full name of the mutual fund scheme |
| category | TEXT | Broad category: Equity or Debt |
| sub_category | TEXT | Sub-category e.g. Large Cap, Small Cap, Gilt |
| plan | TEXT | Regular or Direct plan |
| launch_date | TEXT | Date the scheme was launched |
| benchmark | TEXT | Index used as performance benchmark |
| expense_ratio_pct | REAL | Annual fee charged (0.1% – 2.5%) |
| exit_load_pct | REAL | Fee charged on early redemption |
| min_sip_amount | INTEGER | Minimum SIP investment in INR |
| min_lumpsum_amount | INTEGER | Minimum lumpsum investment in INR |
| fund_manager | TEXT | Name of the fund manager |
| risk_category | TEXT | Risk level: Low/Moderate/High/Very High |
| sebi_category_code | TEXT | SEBI classification code |

## 2. fact_nav (02_nav_history.csv)
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | INTEGER | Foreign key → dim_fund |
| date | TEXT | NAV date (daily) |
| nav | REAL | Net Asset Value in INR |

## 3. fact_transactions (08_investor_transactions.csv)
| Column | Type | Description |
|--------|------|-------------|
| investor_id | TEXT | Unique investor identifier |
| transaction_date | TEXT | Date of transaction |
| amfi_code | INTEGER | Foreign key → dim_fund |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | INTEGER | Transaction amount in INR |
| state | TEXT | Investor's state |
| city | TEXT | Investor's city |
| city_tier | TEXT | City tier (1/2/3) |
| age_group | TEXT | Investor age bracket |
| gender | TEXT | Investor gender |
| annual_income_lakh | REAL | Annual income in lakhs |
| payment_mode | TEXT | UPI / Cheque / Mandate / Net Banking |
| kyc_status | TEXT | Verified / Pending / Rejected |

## 4. fact_performance (07_scheme_performance.csv)
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | INTEGER | Foreign key → dim_fund |
| return_1yr_pct | REAL | 1-year return percentage |
| return_3yr_pct | REAL | 3-year return percentage |
| return_5yr_pct | REAL | 5-year return percentage |
| benchmark_3yr_pct | REAL | Benchmark 3yr return for comparison |
| alpha | REAL | Excess return over benchmark |
| beta | REAL | Market sensitivity (1 = market moves) |
| sharpe_ratio | REAL | Risk-adjusted return metric |
| sortino_ratio | REAL | Downside risk-adjusted return |
| std_dev_ann_pct | REAL | Annualised volatility |
| max_drawdown_pct | REAL | Largest peak-to-trough decline |
| aum_crore | INTEGER | Assets Under Management in crores |
| expense_ratio_pct | REAL | Annual management fee |
| morningstar_rating | INTEGER | Star rating (1–5) |
| risk_grade | TEXT | Risk classification |

## 5. fact_aum (03_aum_by_fund_house.csv)
| Column | Type | Description |
|--------|------|-------------|
| date | TEXT | Reporting date |
| fund_house | TEXT | Name of the AMC |
| aum_lakh_crore | REAL | AUM in lakh crores |
| aum_crore | INTEGER | AUM in crores |
| num_schemes | INTEGER | Number of schemes offered |