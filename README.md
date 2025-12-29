# 📦 Vendor Inventory, Sales & Performance Analytics
[https://github.com/bhavyanjain3004/vendor_performance.github.io/blob/main/vendor_performance_analysis.ipynb](data_analysis)
## 📌 Executive Summary

This project implements an **end-to-end analytics pipeline** to evaluate **vendor performance, inventory efficiency, procurement concentration, and profitability** using large-scale transactional data.

Raw data from purchases, sales, pricing, invoices, and inventory snapshots is ingested into a centralized database, transformed into an **analytics-ready vendor summary table**, and analyzed to generate **actionable business insights** supported by **statistical validation**.

The project mirrors a **real-world data analyst / analytics engineer workflow** and emphasizes:
- Scalable ingestion
- Clean data modeling
- Business-driven KPIs
- Statistical and visual analysis

---

## 🧩 Problem Statement

Organizations working with multiple vendors face challenges such as:
- Over-dependence on a few suppliers
- Capital locked in slow-moving inventory
- Unclear relationship between sales volume and profitability
- Difficulty identifying high-potential brands

This project answers:
- Which vendors and brands drive most revenue?
- Where is procurement risk concentrated?
- Which products are profitable but under-performing?
- Does bulk purchasing reduce unit cost?
- Is there a statistically significant difference between high- and low-performing vendors?

---

## 🗂️ Repository Structure

Vendor-Inventory-Analytics/
│
├── data/
│ ├── purchases.csv
│ ├── purchase_prices.csv
│ ├── vendor_invoice.csv
│ ├── sales.csv
│ ├── begin_inventory.csv
│ ├── end_inventory.csv
│ └── (large files excluded from GitHub)
│
├── logs/
│ ├── ingestion_db.log
│ └── get_vendor_summary.log
│
├── ingestion_db.py
├── get_vendor_summary.py
├── analytics.ipynb
├── vendor_performance_analysis.ipynb
├── inventory.db
└── README.md
> ⚠️ **Note**  
> Two large CSV files were excluded from GitHub due to size constraints.  
> The pipeline automatically ingests them when added locally.

---

## 🧪 Data Sources

| Dataset | Description |
|------|------------|
| `purchases` | Purchase transactions (quantity, dollars, vendor, brand) |
| `purchase_prices` | Brand-level pricing & volume |
| `sales` | Sales quantity, revenue, excise tax |
| `vendor_invoice` | Freight & invoice-level costs |
| `begin_inventory` | Opening inventory snapshot |
| `end_inventory` | Closing inventory snapshot |

---

## ⚙️ Data Ingestion Layer (`ingestion_db.py`)

### Purpose
- Automatically ingest all CSV files from `data/`
- Load them into a centralized SQLite database (`inventory.db`)
- Ensure idempotent, repeatable execution

### Key Design Choices
- `if_exists="replace"` → safe re-runs
- Automatic table naming from filenames
- Centralized logging for observability

### Sample Logs
INFO - Ingesting purchases.csv in db
INFO - Ingesting sales.csv in db
INFO - Ingestion Completed Successfully
Total time taken: ~1.8 minutes
---

## 🧱 Analytical Modeling (`get_vendor_summary.py`)

### Objective
Create a **vendor–brand–level summary table** to avoid repeated joins on large transactional data.

### Core Aggregations
- Total Purchase Quantity & Dollars
- Total Sales Quantity & Dollars
- Freight & Excise Costs

### Derived KPIs
- Gross Profit
- Profit Margin
- Stock Turnover
- Sales-to-Purchase Ratio

### Output Table

This table serves as the **single source of truth** for analytics and dashboards.

---

## 📊 Exploratory Data Analysis (`analytics.ipynb`)

- Validates dataset scale (up to **12.8M rows**)
- Confirms ingestion success
- Performs early sanity checks on schema and distributions

This ensures downstream analysis is built on **clean and verified data**.

---

## 📈 Vendor Performance Analysis (`vendor_performance_analysis.ipynb`)

### Key Analyses Performed

#### 1. Distribution & Outlier Analysis
- Loss-making SKUs identified (negative gross profit)
- Slow-moving inventory detected (zero sales)
- Premium pricing outliers observed

#### 2. Correlation Analysis
- Strong correlation between purchase & sales quantity (≈ 0.999)
- Weak correlation between price and profitability
- High-volume products operate on lower margins

#### 3. Promotional Opportunity Identification
- **198 brands** identified with:
  - High profit margins
  - Low sales volume

#### 4. Top Vendors & Brands
- Sales highly concentrated among global vendors
- Flagship brands dominate revenue contribution

#### 5. Procurement Concentration (Pareto Analysis)
- **Top 10 vendors contribute ~65.7% of total purchases**
- Indicates procurement dependency risk

#### 6. Bulk Purchasing Analysis
- Larger order sizes significantly reduce unit cost
- Confirms economies of scale

#### 7. Inventory Efficiency
- ~$2.71M capital locked in unsold inventory
- Excess stock observed even among top vendors

#### 8. Statistical Validation
- 95% confidence interval analysis
- Welch’s t-test confirms:
  - **Statistically significant difference** in profit margins  
    between high- and low-sales vendors (p < 0.001)

---

## 🧠 Key Business Insights

- High-volume vendors trade margin for scale
- Low-volume vendors maintain premium pricing
- Procurement risk is highly concentrated
- Inventory inefficiencies persist across vendors
- Bulk purchasing is a strong cost optimization lever

---

## 📌 Strategic Recommendations

- Promote high-margin, low-volume brands
- Diversify vendor base to reduce dependency
- Optimize pricing for high-volume SKUs
- Reduce excess inventory for low-turnover vendors
- Leverage bulk procurement strategically

---

## ▶️ How to Run the Project

```bash
pip install pandas numpy matplotlib seaborn sqlalchemy scipy
python ingestion_db.py
python get_vendor_summary.py
Then open:
analytics.ipynb
vendor_performance_analysis.ipynb
