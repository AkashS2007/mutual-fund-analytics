"""
Generate Final PDF Report for Bluestock MF Capstone Project.
"""
import os
import glob
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, HRFlowable
)

# ── Paths ────────────────────────────────────────────────────────
os.makedirs("reports", exist_ok=True)
OUTPUT = "reports/Final_Report.pdf"
CHARTS = "reports/charts"

# ── Styles ───────────────────────────────────────────────────────
styles = getSampleStyleSheet()
BLUE   = colors.HexColor("#1E3A5F")
LBLUE  = colors.HexColor("#00A3E0")
LGRAY  = colors.HexColor("#F5F5F5")

title_style = ParagraphStyle("ReportTitle",
    fontSize=26, textColor=BLUE, spaceAfter=6,
    fontName="Helvetica-Bold", alignment=1)

h1 = ParagraphStyle("H1",
    fontSize=16, textColor=BLUE, spaceBefore=14,
    spaceAfter=6, fontName="Helvetica-Bold")

h2 = ParagraphStyle("H2",
    fontSize=12, textColor=LBLUE, spaceBefore=10,
    spaceAfter=4, fontName="Helvetica-Bold")

body = ParagraphStyle("Body",
    fontSize=10, spaceAfter=6, leading=14,
    fontName="Helvetica")

bullet = ParagraphStyle("Bullet",
    fontSize=10, spaceAfter=4, leading=14,
    leftIndent=20, fontName="Helvetica",
    bulletIndent=10)

def hr(): return HRFlowable(width="100%", thickness=1,
                             color=LBLUE, spaceAfter=8)
def sp(n=8): return Spacer(1, n)

def chart(filename, width=14*cm, caption=""):
    path = os.path.join(CHARTS, filename)
    elems = []
    if os.path.exists(path):
        elems.append(Image(path, width=width,
                           height=width*0.55))
        if caption:
            elems.append(Paragraph(f"<i>{caption}</i>",
                ParagraphStyle("Cap", fontSize=8,
                    textColor=colors.grey, alignment=1)))
    else:
        elems.append(Paragraph(f"[Chart: {filename}]", body))
    return elems

# ── Build Story ──────────────────────────────────────────────────
story = []

# ── Cover Page ───────────────────────────────────────────────────
story += [sp(80)]
story.append(Paragraph("Bluestock Fintech", ParagraphStyle("sub",
    fontSize=14, textColor=LBLUE, alignment=1,
    fontName="Helvetica")))
story += [sp(10)]
story.append(Paragraph("Capstone Project I", title_style))
story.append(Paragraph("Mutual Fund Analytics Platform",
    title_style))
story += [sp(20), hr(), sp(10)]

cover_data = [
    ["Batch",    "MJ28"],
    ["Team",     "akashs3882, bandarivyshnavi2, vhedau47,\nKota Naga Raviteja, divyamadiraju2006"],
    ["Duration", "01 Jun 2026 – 14 Jun 2026"],
    ["Status",   "Completed"],
]
t = Table(cover_data, colWidths=[4*cm, 12*cm])
t.setStyle(TableStyle([
    ("FONTNAME",  (0,0), (-1,-1), "Helvetica"),
    ("FONTNAME",  (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE",  (0,0), (-1,-1), 10),
    ("TEXTCOLOR", (0,0), (0,-1), BLUE),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [LGRAY, colors.white]),
    ("GRID",      (0,0), (-1,-1), 0.5, colors.lightgrey),
    ("PADDING",   (0,0), (-1,-1), 6),
]))
story += [t, PageBreak()]

# ── 1. Executive Summary ─────────────────────────────────────────
story.append(Paragraph("1. Executive Summary", h1))
story.append(hr())
story.append(Paragraph(
    "This report presents the complete analysis of India's mutual fund industry "
    "using 10 AMFI datasets spanning 2022–2026. The project covers 40 fund schemes "
    "across 10 Asset Management Companies (AMCs), analysing 64,320 daily NAV records, "
    "32,778 investor transactions, and portfolio holdings across 12 sub-categories.",
    body))
story.append(Paragraph(
    "Key outcomes include a SQLite star-schema database, 15+ EDA visualisations, "
    "a composite fund scorecard, advanced risk metrics (VaR, CVaR, Rolling Sharpe), "
    "and a 4-page interactive Power BI dashboard.",
    body))

kpis = [
    ["Metric", "Value"],
    ["Total Funds Analysed", "40 schemes across 10 AMCs"],
    ["NAV Records", "64,320 daily records (2022-2026)"],
    ["Investor Transactions", "32,778 across 15 states"],
    ["Total Industry AUM", "Rs. 81 Lakh Crore"],
    ["SIP All-Time High", "Rs. 31,002 Crore (Dec 2025)"],
    ["Total Folios", "26.12 Crore (doubled in 4 years)"],
]
t = Table(kpis, colWidths=[8*cm, 8*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), BLUE),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",    (0,0), (-1,-1), 10),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [LGRAY, colors.white]),
    ("GRID",        (0,0), (-1,-1), 0.5, colors.lightgrey),
    ("PADDING",     (0,0), (-1,-1), 6),
]))
story += [sp(), t, PageBreak()]

# ── 2. Data Sources ───────────────────────────────────────────────
story.append(Paragraph("2. Data Sources", h1))
story.append(hr())
story.append(Paragraph(
    "All datasets were sourced from the Bluestock Fintech internship platform "
    "(Project Documents > Data Sets) and the live mfapi.in API.", body))

ds = [
    ["#", "File", "Description", "Rows"],
    ["1",  "01_fund_master.csv",           "Fund metadata, risk, expense ratio",  "40"],
    ["2",  "02_nav_history.csv",           "Daily NAV 2022-2026",                 "46,000"],
    ["3",  "03_aum_by_fund_house.csv",     "Quarterly AUM by AMC",                "90"],
    ["4",  "04_monthly_sip_inflows.csv",   "Monthly SIP inflow data",             "48"],
    ["5",  "05_category_inflows.csv",      "Category-wise net inflows",           "144"],
    ["6",  "06_industry_folio_count.csv",  "Total industry folios",               "21"],
    ["7",  "07_scheme_performance.csv",    "Risk/return performance metrics",     "40"],
    ["8",  "08_investor_transactions.csv", "Investor transaction records",        "32,778"],
    ["9",  "09_portfolio_holdings.csv",    "Sector/stock holdings",               "322"],
    ["10", "10_benchmark_indices.csv",     "Nifty 50/100 daily index data",       "8,050"],
]
t = Table(ds, colWidths=[1*cm, 5.5*cm, 7.5*cm, 2*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), BLUE),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",    (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [LGRAY, colors.white]),
    ("GRID",        (0,0), (-1,-1), 0.5, colors.lightgrey),
    ("PADDING",     (0,0), (-1,-1), 5),
]))
story += [sp(), t, PageBreak()]

# ── 3. ETL Design ────────────────────────────────────────────────
story.append(Paragraph("3. ETL Design", h1))
story.append(hr())
story.append(Paragraph("3.1 Pipeline Architecture", h2))
story.append(Paragraph(
    "The ETL pipeline follows a structured Extract → Transform → Load approach "
    "orchestrated via run_pipeline.py:", body))
for step in [
    "Extract: Load 10 CSVs using Pandas + fetch live NAV from mfapi.in API",
    "Transform: Clean nav_history (parse dates, forward-fill, remove duplicates), "
     "standardise investor_transactions (transaction types, KYC enums), "
     "validate scheme_performance numeric ranges",
    "Load: Insert cleaned data into SQLite star-schema (bluestock_mf.db) "
     "using SQLAlchemy",
    "Validate: Confirm all 40 AMFI codes match between fund_master and nav_history",
]:
    story.append(Paragraph(f"• {step}", bullet))

story.append(Paragraph("3.2 Star Schema Design", h2))
story.append(Paragraph(
    "The database follows a star schema with dim_fund and dim_date as "
    "dimension tables, and fact_nav, fact_transactions, fact_performance, "
    "fact_aum as fact tables. All fact tables reference dim_fund via amfi_code.", body))

schema_data = [
    ["Table",               "Type",      "Rows",   "Key Columns"],
    ["dim_fund",            "Dimension", "40",     "amfi_code (PK)"],
    ["fact_nav",            "Fact",      "64,320", "amfi_code (FK), date, nav"],
    ["fact_transactions",   "Fact",      "32,778", "amfi_code (FK), amount_inr"],
    ["fact_performance",    "Fact",      "40",     "amfi_code (FK), sharpe_ratio"],
    ["fact_aum",            "Fact",      "90",     "fund_house, aum_crore"],
]
t = Table(schema_data, colWidths=[5*cm, 3*cm, 3*cm, 5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), BLUE),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",    (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [LGRAY, colors.white]),
    ("GRID",        (0,0), (-1,-1), 0.5, colors.lightgrey),
    ("PADDING",     (0,0), (-1,-1), 5),
]))
story += [sp(), t, PageBreak()]

# ── 4. EDA Findings ───────────────────────────────────────────────
story.append(Paragraph("4. EDA Findings", h1))
story.append(hr())

findings = [
    ("NAV Trend Analysis",
     "All 40 funds showed strong NAV appreciation during the 2023 bull run, "
     "with small-cap funds gaining 35-45%. A mild correction in mid-2024 was "
     "followed by recovery through 2025.",
     "01_nav_trends.png"),
    ("AUM Growth",
     "SBI Mutual Fund dominates industry AUM at Rs. 12.5 Lakh Crore, nearly "
     "3x its closest competitor. Total industry AUM grew from Rs. 38L Cr "
     "to Rs. 81L Cr between 2022-2025.",
     "02_aum_growth.png"),
    ("SIP Inflow Trends",
     "Monthly SIP inflows grew consistently from Rs. 11,517 Cr (Jan 2022) to "
     "an all-time high of Rs. 31,002 Cr (Dec 2025), reflecting growing retail "
     "investor participation.",
     "03_sip_trend.png"),
    ("Category Inflows",
     "Flexi Cap and Small Cap categories attract the highest net inflows, "
     "while Gilt and Liquid funds see seasonal patterns tied to interest rate cycles.",
     "04_category_heatmap.png"),
]

for title_text, desc, chart_file in findings:
    story.append(Paragraph(title_text, h2))
    story.append(Paragraph(desc, body))
    story += chart(chart_file, caption=f"Figure: {title_text}")
    story.append(sp())

story.append(PageBreak())

# ── 5. Performance Analysis ───────────────────────────────────────
story.append(Paragraph("5. Performance Analysis", h1))
story.append(hr())
story.append(Paragraph("5.1 Key Metrics Computed", h2))
for m in [
    "Daily Returns: daily_return = NAV_t / NAV_t-1 - 1 for all 40 schemes",
    "CAGR: Computed for 1yr, 3yr, 5yr horizons using (NAV_end/NAV_start)^(1/n) - 1",
    "Sharpe Ratio: (Rp - Rf) / Std(Rp) x sqrt(252), Rf = 6.5% RBI repo rate",
    "Sortino Ratio: Same as Sharpe but denominator uses only downside std deviation",
    "Alpha & Beta: OLS regression of fund returns on Nifty 100 returns",
    "Maximum Drawdown: min(NAV / running_max - 1) for each fund",
    "VaR (95%): 5th percentile of daily return distribution",
    "CVaR (95%): Mean of returns below VaR threshold",
]:
    story.append(Paragraph(f"• {m}", bullet))

story.append(Paragraph("5.2 Fund Scorecard Methodology", h2))
story.append(Paragraph(
    "A composite score (0-100) was computed using weighted percentile ranks:", body))
scorecard_data = [
    ["Component",           "Weight", "Direction"],
    ["3-Year CAGR Rank",    "30%",    "Higher is better"],
    ["Sharpe Ratio Rank",   "25%",    "Higher is better"],
    ["Alpha Rank",          "20%",    "Higher is better"],
    ["Expense Ratio Rank",  "15%",    "Lower is better (inverse)"],
    ["Max Drawdown Rank",   "10%",    "Lower is better (inverse)"],
]
t = Table(scorecard_data, colWidths=[7*cm, 3*cm, 6*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), BLUE),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",    (0,0), (-1,-1), 10),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [LGRAY, colors.white]),
    ("GRID",        (0,0), (-1,-1), 0.5, colors.lightgrey),
    ("PADDING",     (0,0), (-1,-1), 6),
]))
story += [sp(), t]
story += chart("P_benchmark_comparison.png",
               caption="Figure: Top 5 Funds vs Nifty 50 & Nifty 100 (3-Year Indexed)")
story.append(PageBreak())

# ── 6. Investor Analytics ─────────────────────────────────────────
story.append(Paragraph("6. Investor Analytics", h1))
story.append(hr())
for point in [
    "Demographics: 25-35 age group dominates SIP investments (42%). "
     "Male investors outnumber female 2:1 across all transaction types.",
    "Geography: Maharashtra and Karnataka lead in SIP volumes. "
     "T30 cities account for 65% of total investments.",
    "SIP Continuity: 18% of investors with 6+ SIPs flagged as at-risk "
     "(avg gap > 35 days), representing potential churn.",
    "Cohort Analysis: 2024 cohort shows highest avg SIP amount, "
     "suggesting newer investors commit larger amounts.",
    "Transaction Split: SIP transactions dominate (68%), followed by "
     "Lumpsum (22%) and Redemptions (10%).",
]:
    story.append(Paragraph(f"• {point}", bullet))
story += chart("05_demographics.png",
               caption="Figure: Investor Demographics — Age, Amount, Gender")
story += chart("06_geographic.png",
               caption="Figure: Geographic Distribution by State and City Tier")
story.append(PageBreak())

# ── 7. Limitations ────────────────────────────────────────────────
story.append(Paragraph("7. Limitations", h1))
story.append(hr())
for lim in [
    "Dataset is synthetic/sample data — real AMFI data may show different patterns",
    "Live NAV API (mfapi.in) codes did not fully match project dataset AMFI codes",
    "Power BI dashboard requires desktop app — no web embed without Power BI Pro",
    "VaR computation assumes historical distribution — does not account for tail risk",
    "SIP continuity analysis limited to transaction gaps — does not track mandate status",
]:
    story.append(Paragraph(f"• {lim}", bullet))

story += [sp(20)]

# ── 8. Recommendations ────────────────────────────────────────────
story.append(Paragraph("8. Recommendations", h1))
story.append(hr())
for rec in [
    "AMCs should target at-risk SIP investors (18%) with automated reminders "
     "30 days after last transaction to reduce churn",
    "Small Cap and Flexi Cap funds should be highlighted in investor communications "
     "given consistent inflow growth and superior 3-year returns",
    "B30 city investors (35%) represent an underserved growth opportunity — "
     "digital-first SIP campaigns recommended",
    "Funds with HHI > 0.15 (concentrated sector bets) should disclose "
     "concentration risk more prominently in fund factsheets",
    "Rolling Sharpe monitoring should be implemented as an early warning system "
     "for fund performance deterioration",
]:
    story.append(Paragraph(f"• {rec}", bullet))

story.append(PageBreak())

# ── 9. Conclusion ─────────────────────────────────────────────────
story.append(Paragraph("9. Conclusion", h1))
story.append(hr())
story.append(Paragraph(
    "This capstone project successfully demonstrates end-to-end data analytics "
    "capabilities applied to India's mutual fund industry. From raw CSV ingestion "
    "to an interactive Power BI dashboard, the pipeline covers ETL, SQL design, "
    "EDA, financial metrics, advanced risk analytics, and business insights.",
    body))
story.append(Paragraph(
    "The mutual fund industry's strong growth trajectory — doubling folios, "
    "SIP inflows at all-time highs, and AUM crossing Rs. 81L Cr — presents "
    "significant opportunities for data-driven decision making by AMCs, "
    "distributors, and regulators alike.",
    body))
story += [sp(30)]
story.append(Paragraph("Submitted by Team MJ28 | Bluestock Fintech Internship | June 2026",
    ParagraphStyle("footer", fontSize=9, textColor=colors.grey, alignment=1)))

# ── Build PDF ────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)
doc.build(story)
print(f"✅ Report saved → {OUTPUT}")