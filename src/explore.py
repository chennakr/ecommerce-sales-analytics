from pathlib import Path
import sqlite3
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/"sales.db"

def main():
    if not DB.exists():
        print("Run `python src/pipeline.py` first.")
        return
    queries={
        "Monthly revenue":"""SELECT substr(order_date,1,7) month,
        ROUND(SUM(quantity*unit_price),2) revenue FROM sales
        GROUP BY month ORDER BY month""",
        "Top 5 products":"""SELECT product_name, ROUND(SUM(quantity*unit_price),2) revenue
        FROM sales GROUP BY product_id ORDER BY revenue DESC LIMIT 5""",
        "Revenue by region":"""SELECT region, ROUND(SUM(quantity*unit_price),2) revenue
        FROM sales GROUP BY region ORDER BY revenue DESC""",
    }
    with sqlite3.connect(DB) as conn:
        for title,sql in queries.items():
            print("\n"+title+"\n"+"-"*len(title))
            print(pd.read_sql_query(sql,conn).to_string(index=False))

if __name__=="__main__":
    main()
