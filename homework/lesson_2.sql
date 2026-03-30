-- Lesson 2.1: Вывести названия товаров и общее количество продаж для каждого товара
SELECT p.name, SUM(s.quantity) as total_quantity
FROM products p
JOIN sales s ON p.id = s.product_id
GROUP BY p.name;

-- Lesson 2.2: Найти товары с общей суммой продаж более 500
SELECT p.name, SUM(s.quantity * p.price) as total_revenue
FROM products p
JOIN sales s ON p.id = s.product_id
GROUP BY p.name
HAVING total_revenue > 500;
