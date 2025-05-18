SELECT Brand, Category, Description, total
FROM sales
WHERE total >= 50
GROUP BY Category
ORDER BY total DESC;