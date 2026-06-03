-- ─── QUERY 1: Top 5 funds by AUM ────────────────────────────────
SELECT scheme_name, fund_house, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- ─── QUERY 2: Average NAV per month for each fund ───────────────
SELECT amfi_code,
       strftime('%Y-%m', date) AS month,
       ROUND(AVG(nav), 4) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

-- ─── QUERY 3: SIP inflow YoY growth ────────────────────────────
SELECT month,
       sip_inflow_crore,
       yoy_growth_pct
FROM monthly_sip_inflows
ORDER BY month;

-- ─── QUERY 4: Transactions by state ────────────────────────────
SELECT state,
       COUNT(*) AS total_transactions,
       SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;

-- ─── QUERY 5: Funds with expense ratio < 1% ─────────────────────
SELECT scheme_name, fund_house, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- ─── QUERY 6: Best performing funds by 3yr return ───────────────
SELECT f.scheme_name, f.fund_house, p.return_3yr_pct, p.alpha, p.sharpe_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.return_3yr_pct DESC
LIMIT 10;

-- ─── QUERY 7: Transaction breakdown by type and gender ──────────
SELECT transaction_type,
       gender,
       COUNT(*) AS count,
       ROUND(AVG(amount_inr), 2) AS avg_amount
FROM fact_transactions
GROUP BY transaction_type, gender
ORDER BY transaction_type, gender;

-- ─── QUERY 8: AUM growth by fund house over time ────────────────
SELECT fund_house,
       date,
       aum_crore
FROM fact_aum
ORDER BY fund_house, date;

-- ─── QUERY 9: Top 5 funds by Sharpe ratio (risk-adjusted) ───────
SELECT f.scheme_name, f.risk_category,
       p.sharpe_ratio, p.sortino_ratio, p.max_drawdown_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.sharpe_ratio DESC
LIMIT 5;

-- ─── QUERY 10: Investor age group vs avg investment amount ───────
SELECT age_group,
       COUNT(*) AS total_investors,
       ROUND(AVG(amount_inr), 2) AS avg_investment,
       SUM(amount_inr) AS total_invested
FROM fact_transactions
GROUP BY age_group
ORDER BY avg_investment DESC;