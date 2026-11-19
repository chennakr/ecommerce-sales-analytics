-- 1. Revenue by month
SELECT substr(order_date, 1, 7) AS month,
       ROUND(SUM(quantity * unit_price), 2) AS revenue,
       SUM(quantity) AS units_sold,
       COUNT(*) AS orders
FROM sales
GROUP BY month
ORDER BY month;

-- 2. Top products by revenue
SELECT product_name, category,
       SUM(quantity) AS units_sold,
       ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM sales
GROUP BY product_id, product_name, category
ORDER BY revenue DESC
LIMIT 10;

-- 3. Revenue by category
SELECT category,
       ROUND(SUM(quantity * unit_price), 2) AS revenue,
       SUM(quantity) AS units_sold
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- 4. Revenue by region
SELECT region, ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- 5. Top customers by spend
SELECT customer_id,
       ROUND(SUM(quantity * unit_price), 2) AS lifetime_spend,
       COUNT(*) AS order_count
FROM sales
GROUP BY customer_id
ORDER BY lifetime_spend DESC
LIMIT 10;

-- 6. Average order value (each row is one order in this demo dataset)
SELECT ROUND(AVG(quantity * unit_price), 2) AS average_order_value
FROM sales;

-- 7. Month-over-month revenue change using a window function
WITH monthly AS (
    SELECT substr(order_date, 1, 7) AS month,
           SUM(quantity * unit_price) AS revenue
    FROM sales
    GROUP BY month
)
SELECT month,
       ROUND(revenue, 2) AS revenue,
       ROUND(revenue - LAG(revenue) OVER (ORDER BY month), 2) AS change_from_previous_month
FROM monthly
ORDER BY month;

-- 8. Repeat customer count
SELECT COUNT(*) AS repeat_customers
FROM (
    SELECT customer_id
    FROM sales
    GROUP BY customer_id
    HAVING COUNT(*) > 1
);
