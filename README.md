# E-commerce Sales Analytics (Python + SQL)

A runnable portfolio project that demonstrates a small data analytics pipeline:
CSV ingestion → data cleaning/validation → SQLite → analytical SQL → charts and report.

## Skills demonstrated
- Python, Pandas, reusable functions
- Data cleaning: invalid dates, missing values, invalid quantities, duplicate records
- SQL schema design, aggregations, CTEs, window functions (`LAG`)
- SQLite database integration
- Data visualization with Matplotlib
- Reproducible command-line project structure

## Dataset
`data/sales_raw.csv` is synthetic practice data. It contains intentionally messy rows so the cleaning pipeline can demonstrate validation and deduplication. Do not present synthetic findings as real company data.

## Setup

Python 3.10+ recommended.

### Windows (PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/pipeline.py
python src/explore.py
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/pipeline.py
python src/explore.py
```

## Output
Running the pipeline creates:
- `sales.db` — SQLite database
- `reports/monthly_revenue.png`
- `reports/category_revenue.png`
- `reports/summary.txt`

The script recreates the database each run so results are reproducible.

## SQL practice
Open `sql/analysis_queries.sql` in a SQL editor or run each query against `sales.db`. It includes monthly revenue, product/category/region performance, top customers, average order value, month-over-month changes using `LAG`, and repeat customers.

## Portfolio improvements (your next iterations)
1. Add tests for cleaning logic (`pytest`).
2. Add a customer table and product table, then normalize the database.
3. Add order-level metrics and clarify whether rows represent line items or orders.
4. Build a dashboard in Power BI or Streamlit.
5. Replace the synthetic CSV with a public dataset and document its source.
6. Add logging, config, and automated scheduled execution.

## Suggested resume bullet (only after running and verifying)
Built a Python/Pandas analytics pipeline to clean and validate sales records, load them into SQLite, and analyze revenue performance using SQL aggregations and window functions; generated monthly/category visualizations and an automated summary report.
