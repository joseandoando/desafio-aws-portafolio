-- Example Athena queries over the curated Glue table.

-- Revenue and number of orders by month
SELECT
    year,
    month,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(total_amount), 2) AS revenue
FROM curated_sales
GROUP BY year, month
ORDER BY year, month;

-- Top products by revenue
SELECT
    product,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total_amount), 2) AS revenue
FROM curated_sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 10;

-- Average order value
SELECT
    ROUND(AVG(order_total), 2) AS average_order_value
FROM (
    SELECT order_id, SUM(total_amount) AS order_total
    FROM curated_sales
    GROUP BY order_id
);
