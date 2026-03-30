-- Lesson 2.1: Вывести названия товаров и общее количество продаж с дополнительной информацией
SELECT 
    p.name,
    p.category,
    SUM(s.quantity) as total_quantity,
    COUNT(s.id) as transaction_count,
    MIN(s.date) as first_sale,
    MAX(s.date) as last_sale
FROM products p
JOIN sales s ON p.id = s.product_id
GROUP BY p.id, p.name, p.category
ORDER BY total_quantity DESC;

-- Lesson 2.2: Найти товары с общей суммой продаж более 500 с детальной статистикой
SELECT 
    p.name,
    p.category,
    SUM(s.quantity * p.price) as total_revenue,
    SUM(s.quantity) as total_sold,
    AVG(s.quantity) as avg_per_transaction,
    COUNT(DISTINCT s.date) as days_sold
FROM products p
JOIN sales s ON p.id = s.product_id
GROUP BY p.id, p.name, p.category
HAVING SUM(s.quantity * p.price) > 500
ORDER BY total_revenue DESC;
