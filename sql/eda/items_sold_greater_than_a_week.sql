-- Find items that took longer than a week to sell--
SELECT 
    sales.order_id, 
    sales.Category, 
    sales.Size, 
    summary.time_to_sell_days, 
    summary."Net Earnings"
FROM 
    sales
JOIN 
    summary ON sales.order_id = summary.order_id
WHERE 
    summary.time_to_sell_days > 7
ORDER BY 
    summary.time_to_sell_days ASC;


