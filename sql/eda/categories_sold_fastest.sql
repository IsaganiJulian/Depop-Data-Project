--Find categories that sold the fastest--
SELECT sales.Category, AVG(summary.time_to_sell_days) as average_sell_days
FROM sales
JOIN summary on sales.order_id = summary.order_id
GROUP BY sales.Category
ORDER BY average_sell_days ASC;