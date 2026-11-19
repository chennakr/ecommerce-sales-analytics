from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sales_raw.csv"
DB = ROOT / "sales.db"
REPORTS = ROOT / "reports"
SCHEMA = ROOT / "sql" / "schema.sql"
QUERIES = ROOT / "sql" / "analysis_queries.sql"

def clean_data(path=DATA):
    df = pd.read_csv(path)
    initial_rows = len(df)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.dropna(subset=["order_id", "order_date", "customer_id", "product_id",
                           "product_name", "category", "quantity", "unit_price", "region"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] >= 0)]
    df = df.drop_duplicates(subset=["order_id"])
    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].round(2)
    cleaned_rows = len(df)
    return df, initial_rows, cleaned_rows

def load_database(df):
    with sqlite3.connect(DB) as conn:
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        df.to_sql("sales", conn, if_exists="append", index=False)
    print(f"Loaded {len(df):,} cleaned rows into {DB.name}")

def run_query(sql):
    with sqlite3.connect(DB) as conn:
        return pd.read_sql_query(sql, conn)

def make_charts():
    REPORTS.mkdir(exist_ok=True)
    monthly_sql = """SELECT substr(order_date,1,7) month,
    ROUND(SUM(quantity*unit_price),2) revenue FROM sales GROUP BY month ORDER BY month"""
    monthly = run_query(monthly_sql)
    plt.figure(figsize=(10,5))
    plt.plot(monthly["month"], monthly["revenue"], marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month"); plt.ylabel("Revenue")
    plt.xticks(rotation=45); plt.tight_layout()
    plt.savefig(REPORTS/"monthly_revenue.png", dpi=150); plt.close()

    category_sql = """SELECT category, SUM(quantity*unit_price) revenue
    FROM sales GROUP BY category ORDER BY revenue DESC"""
    category = run_query(category_sql)
    plt.figure(figsize=(8,5))
    plt.bar(category["category"], category["revenue"])
    plt.title("Revenue by Category")
    plt.xlabel("Category"); plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(REPORTS/"category_revenue.png", dpi=150); plt.close()
    return monthly, category

def create_report(initial, cleaned, monthly, category):
    total_revenue = run_query("SELECT ROUND(SUM(quantity*unit_price),2) total FROM sales").iloc[0,0]
    orders = run_query("SELECT COUNT(*) n FROM sales").iloc[0,0]
    customers = run_query("SELECT COUNT(DISTINCT customer_id) n FROM sales").iloc[0,0]
    top_product = run_query("""SELECT product_name, ROUND(SUM(quantity*unit_price),2) revenue
                               FROM sales GROUP BY product_id ORDER BY revenue DESC LIMIT 1""").iloc[0]
    top_category = category.iloc[0]
    best_month = monthly.loc[monthly["revenue"].idxmax()]
    report = f"""ECOMMERCE SALES ANALYTICS — SUMMARY

Data quality:
- Input rows: {initial:,}
- Rows retained after cleaning: {cleaned:,}
- Rows removed: {initial-cleaned:,}

Key metrics:
- Total revenue: ${total_revenue:,.2f}
- Valid orders: {orders:,}
- Unique customers: {customers:,}
- Highest revenue product: {top_product['product_name']} (${top_product['revenue']:,.2f})
- Highest revenue category: {top_category['category']} (${top_category['revenue']:,.2f})
- Best month: {best_month['month']} (${best_month['revenue']:,.2f})

Charts saved in reports/:
- monthly_revenue.png
- category_revenue.png

Note: this is synthetic practice data, not actual company performance.
"""
    (REPORTS/"summary.txt").write_text(report,encoding="utf-8")
    print(report)

def main():
    REPORTS.mkdir(exist_ok=True)
    df, initial, cleaned = clean_data()
    load_database(df)
    monthly, category = make_charts()
    create_report(initial, cleaned, monthly, category)
    print("Pipeline complete. See reports/ and sales.db.")

if __name__ == "__main__":
    main()
