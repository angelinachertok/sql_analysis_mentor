-- Lesson 1.1: Вывести все товары из категории 'Fruits' с сортировкой по цене
SELECT id, name, price, category 
FROM products 
WHERE category = 'Fruits' 
ORDER BY price DESC;

-- Lesson 1.2: Посчитать общую сумму продаж для каждого товара с фильтрацией
SELECT p.id, p.name, SUM(s.quantity) as total_quantity
FROM products p
JOIN sales s ON p.id = s.product_id
GROUP BY p.id, p.name
HAVING SUM(s.quantity) > 0
ORDER BY total_quantity DESC;
