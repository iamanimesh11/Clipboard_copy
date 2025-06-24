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

with cte as(
select count(customer_id) as product_bought_often ,customer_id,
        product_name
      from customer_orders 
      group by product_name ,customer_id
      having product_bought_often >2
      )
,
cte2 as ( select product_bought_often,customer_id,product_name,
rank() over ( partition by customer_id  order by product_bought_often desc) as rn
from cte)

select * from cte2
where rn=1
