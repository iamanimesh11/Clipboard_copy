-- Create the tables first
CREATE TABLE users (
    user_id INT PRIMARY KEY,  signup_date DATE NOT NULL
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,user_id INT NOT NULL,order_date DATE NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- Insert data into the tables
INSERT INTO users (user_id, signup_date) VALUES (101, '2024-01-01'), (102, '2024-01-10'),(103, '2024-02-15');
INSERT INTO orders (order_id, user_id, order_date, amount) VALUES (1, 101, '2024-01-05', 200),(2, 101, '2024-02-10', 300),(3, 102, '2024-01-15', 150),
(4, 103, '2024-03-01', 500),(5, 101, '2024-03-20', 250);

with cte as(
select u.*,o.order_date,o.amount from users u join orders o on u.user_id=o.user_id
),

cte2 as (
select *,
LAG(order_date) over (partition by user_id order by order_date) as prev_Date,
DATEDIFF(order_date,LAG(order_date) over (partition by user_id order by order_date)) as days 
from cte
)

select user_id,count(order_date) as total_orders,sum(amount) as total_Spend,avg(days),max(order_date),
case when DATEDIFF(CURDATE(),max(order_date)) >60 then "high risk" else "Active" end as churn_risk_flag ,
case when sum(amount)>= 1000 then 'Gold' when sum(amount)<=500 then "silver" 
else 'Bronze' end as loyaly_tier
from cte2
group by user_id






†**************

-- Create the 'users' table
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    signup_date DATE
);

-- Insert data into the 'users' table
INSERT INTO users (user_id, signup_date) VALUES
(101, '2024-01-15'),
(102, '2024-02-05'),
(103, '2024-02-28'),
(104, '2024-03-10');

-- Create the 'orders' table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    order_date DATE,
    amount DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Insert data into the 'orders' table
INSERT INTO orders (order_id, user_id, order_date, amount) VALUES
(1, 101, '2024-01-20', 100),
(2, 101, '2024-02-10', 120),
(3, 101, '2024-03-05', 200),
(4, 102, '2024-02-10', 80),
(5, 102, '2024-03-12', 120),
(6, 103, '2024-03-15', 90),
(7, 104, '2024-03-18', 150),
(8, 104, '2024-04-20', 160),
(9, 104, '2024-05-22', 200);


