-- Sales based on Size excluding shoe size 
SELECT  Size, COUNT(*) as size_count
FROM sales
WHERE size <> 'US 8.5'
GROUP BY  Size
ORDER BY size_count DESC;