CREATE TABLE customer_orders (
    order_id INT PRIMARY KEY,
    customer_id VARCHAR(50),
    product_name VARCHAR(255),
    order_date DATE
);

INSERT INTO customer_orders (order_id, customer_id, product_name, order_date) VALUES
    (1, 'C001', 'Milk', '2024-01-01'),
    (2, 'C001', 'Milk', '2024-01-10'),
    (3, 'C001', 'Eggs', '2024-01-15'),
    (4, 'C001', 'Milk', '2024-02-01'),
    (5, 'C002', 'Bread', '2024-01-05'),
    (6, 'C002', 'Bread', '2024-02-10'),
    (7, 'C002', 'Jam', '2024-02-25'),
    (8, 'C003', 'Butter', '2024-02-01'),
    (9, 'C003', 'Butter', '2024-02-15'),
    (10, 'C003', 'Butter', '2024-03-01'),
    (11, 'C003', 'Milk', '2024-03-10');


INSERT INTO customer_orders (order_id, customer_id, product_name, order_date) VALUES
    (12, 'C001', 'Bread', '2024-03-05'),
    (13, 'C002', 'Eggs', '2024-03-15'),
    (14, 'C004', 'Yogurt', '2024-01-20'),
    (15, 'C004', 'Cheese', '2024-02-05'),
    (16, 'C001', 'Coffee', '2024-03-20'),
    (17, 'C005', 'Apples', '2024-02-10'),
    (18, 'C005', 'Oranges', '2024-02-12'),
    (19, 'C002', 'Milk', '2024-04-01'),
    (20, 'C004', 'Yogurt', '2024-03-01');
