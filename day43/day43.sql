-- CREATE TABLE
CREATE TABLE IF NOT EXISTS sales (
    order_id INTEGER,
    customer_id INTEGER,
    region TEXT,
    product TEXT,
    quantity INTEGER,
    price REAL,
    order_date TEXT
);

-- INSERT DATA
INSERT INTO sales VALUES
(1, 101, 'North', 'Laptop', 2, 60000, '2024-01-10'),
(2, 102, 'South', 'Phone', 3, 20000, '2024-01-12'),
(3, 103, 'East', 'Tablet', 1, 30000, '2024-01-15'),
(4, 101, 'North', 'Phone', 2, 20000, '2024-02-01'),
(5, 104, 'West', 'Laptop', 1, 60000, '2024-02-10'),
(6, 105, 'South', 'Tablet', 2, 30000, '2024-02-15'),
(7, 106, 'East', 'Phone', 4, 20000, '2024-03-01');

-- TOTAL SALES
SELECT SUM(quantity * price) AS total_sales
FROM sales;


-- SALES BY REGION
SELECT region, SUM(quantity * price) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC;

-- TOP SELLING PRODUCT
SELECT product, SUM(quantity) AS total_quantity
FROM sales
GROUP BY product
ORDER BY total_quantity DESC
LIMIT 1;

-- MONTHLY SALES TREND
SELECT 
    strftime('%Y-%m', order_date) AS month,
    SUM(quantity * price) AS monthly_sales
FROM sales
GROUP BY month
ORDER BY month;

-- CUSTOMER SPENDING
SELECT customer_id, SUM(quantity * price) AS total_spent
FROM sales
GROUP BY customer_id
ORDER BY total_spent DESC;

-- AVERAGE ORDER VALUE
SELECT AVG(quantity * price) AS avg_order_value
FROM sales;

-- HIGH VALUE ORDERS
SELECT *
FROM sales
WHERE (quantity * price) > 50000;