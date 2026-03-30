-- Lesson 1.1: Вывести все товары из категории 'Fruits'
SELECT * FROM products WHERE category = 'Fruits';

-- Lesson 1.2: Посчитать общую сумму продаж для каждого товара
SELECT product_id, SUM(quantity) as total_quantity 
FROM sales 
GROUP BY product_id;
