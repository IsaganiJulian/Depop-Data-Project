-- Summary statistics for Item Price
SELECT 
COUNT(*) as total_rows,
AVG("Item price") AS avg_value,
MAX("Item price") AS max_value,
MIN("Item price") AS min_value
FROM sales;
