-- Step 1: Create a sample table with some fake sales data
CREATE OR REPLACE TABLE Practice.sales_data_temp AS
SELECT 
  DATE '2023-01-01' AS order_date, 'A101' AS customer_id, 'Electronics' AS category, 500 AS amount UNION ALL
SELECT DATE '2023-01-01', 'A102', 'Clothing', 150 UNION ALL
SELECT DATE '2023-01-02', 'A101', 'Electronics', 200 UNION ALL
SELECT DATE '2023-01-02', 'A103', 'Books', 80 UNION ALL
SELECT DATE '2023-01-03', 'A104', 'Clothing', 220 UNION ALL
SELECT DATE '2023-01-03', 'A102', 'Books', 120 UNION ALL
SELECT DATE '2023-01-04', 'A105', 'Electronics', 900;



-- Step 2: Create a PARTITIONED + CLUSTERED table
CREATE OR REPLACE TABLE Practice.sales_data
PARTITION BY order_date
CLUSTER BY customer_id, category AS
SELECT * FROM Practice.sales_data_temp;





-- Step 3: Query with partition pruning (only scans one partition)
SELECT *
FROM Practice.sales_data
WHERE order_date = '2023-01-02';






-- Step 4: Query with clustering benefit
SELECT *
FROM Practice.sales_data
WHERE customer_id = 'A101'
  AND order_date BETWEEN '2023-01-01' AND '2023-01-03';