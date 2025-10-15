
CREATE TABLE users (user_id INT PRIMARY KEY,signup_date DATE NOT NULL,plan_type VARCHAR(50) NOT NULL);

CREATE TABLE orders (
order_id INT PRIMARY KEY,user_id INT NOT NULL,order_date DATE NOT NULL,product_category VARCHAR(100) NOT NULL,amount NUMERIC(10, 2) NOT NULL,
dynamic_price NUMERIC(10, 2) NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id));

CREATE TABLE user_events (
event_id INT PRIMARY KEY,user_id INT NOT NULL,event_type VARCHAR(50) NOT NULL, 
event_time TIMESTAMP NOT NULL,FOREIGN KEY (user_id) REFERENCES users(user_id));

INSERT INTO users (user_id, signup_date, plan_type) VALUES (101, '2024-01-15', 'basic'),(102, '2024-01-20', 'premium'),(103, '2024-02-05', 'basic'),(104, '2024-02-10', 'premium'),(105, '2024-03-01', 'basic'),(106, '2024-03-03', 'enterprise'),(107, '2024-03-05', 'basic'),(108, '2024-04-01', 'premium'),(109, '2024-04-05', 'basic'),(110, '2024-04-10', 'premium');

INSERT INTO orders (order_id, user_id, order_date, product_category, amount, dynamic_price) VALUES (5001, 101, '2024-01-16', 'electronics', 150.00, 145.00),(5002, 102, '2024-01-21', 'books', 25.50, 25.50),(5003, 101, '2024-02-01', 'electronics', 160.00, 160.00),(5004, 103, '2024-02-06', 'home_goods', 75.00, 70.00),(5005, 101, '2024-03-02', 'books', 30.00, 31.00),(5006, 105, '2024-03-05', 'electronics', 200.00, 210.00),(5007, 106, '2024-03-04', 'home_goods', 50.00, 50.00),(5008, 108, '2024-04-02', 'electronics', 180.00, 185.00),
(5009, 102, '2024-04-03', 'books', 28.00, 28.00),(5010, 109, '2024-04-06', 'home_goods', 85.00, 80.00),(5011, 102, '2024-04-15', 'books', 28.00, 35.00), (5012, 104, '2024-04-20', 'electronics', 300.00, 305.00),(5013, 101, '2024-04-25', 'electronics', 155.00, 160.00),(5014, 107, '2024-02-01', 'widgets', 10.00, 10.00),(5015, 107, '2024-03-01', 'widgets', 5.00, 5.00),(5016, 108, '2024-04-01', 'gizmos', 50.00, 50.00);

INSERT INTO user_events (event_id, user_id, event_type, event_time) VALUES (8001, 101, 'browse', '2024-01-15 10:05:00'),(8002, 101, 'add_to_cart', '2024-01-15 10:07:30'),(8003, 101, 'purchase', '2024-01-16 09:00:00'),(8004, 103, 'browse', '2024-02-05 15:00:00'),(8005, 103, 'add_to_cart', '2024-02-05 15:02:00'),(8006, 103, 'abandon_cart', '2024-02-05 15:05:00'),(8007, 104, 'browse', '2024-02-10 11:30:00'),(8008, 104, 'add_to_cart', '2024-02-10 11:35:00'),(8009, 104, 'purchase', '2024-02-10 11:40:00'),(8010, 105, 'browse', '2024-03-01 10:00:00'),(8011, 105, 'purchase', '2024-03-05 09:00:00'),(8012, 107, 'browse', '2024-03-05 14:00:00'),(8013, 107, 'browse', '2024-03-05 14:02:00'),(8014, 102, 'browse', '2024-04-02 11:00:00'),
(8015, 102, 'add_to_cart', '2024-04-02 11:05:00'),(8016, 102, 'purchase', '2024-04-03 08:00:00'),(8017, 108, 'browse', '2024-04-01 10:00:00'),(8018, 108, 'purchase', '2024-04-02 10:00:00');


-- 4. Top Retention Users per Plan:
-- Users with highest repeat orders in last 90 days, rank them by frquency and total spend



with cte as (
select user_id,order_date,
TIMESTAMPdiff(day,order_date,lag(order_date) over( partition by user_id order by order_date ))
as prev_order_Date,
amount
from orders order by user_id
)

select user_id ,count(order_date)-1 as total_repeating_orders,sum(amount) as total_amount
from cte 
group by user_id
order by count(order_date)- 1 desc  ,total_amount desc 




-- 3. Revenue Anomalies:
-- Compare dynamic price vs base price across products.
-- Flag products where revenue per unit changed >50% vs last month.

-- with monthly_Revenue as (
-- select product_category,date_format(order_date,'%Y-%m') as order_month,
-- round(avg(amount),2) as avg_Revenue_per_order,
-- round(avg(dynamic_price),2) as avg_dynamic_price
-- from orders
-- group by product_category ,
-- date_format(order_date,'%Y-%m')
-- order by product_category
-- ),

-- compare_changes as (
-- select * ,
-- lag(avg_Revenue_per_order) over 
--   (partition by product_category
--   order by order_month) as prev_revenue_per_order
--   from monthly_Revenue )

-- select *,
-- round(((avg_Revenue_per_order-prev_revenue_per_order)/prev_revenue_per_order)*100
-- ,2)as pct_change,
-- case when 
-- abs((avg_Revenue_per_order-prev_revenue_per_order)/prev_revenue_per_order)>0.5 then 'anomaly'
-- else 'normmal'end as anomaly_flag
-- from compare_changes
-- where prev_revenue_per_order is not null 
-- order by product_category,order_month













-- -- behavioral _analysis

-- -- 2. Behavioral Funnels:
-- -- For each user, sequence their events.]
-- -- Identify users who dropped off at each funnel step.
-- -- Compute time spent between steps.
-- WITH ordered_events AS(
-- select user_id,event_type,event_time,
-- case when event_type ='browse' then 1 
-- when event_type='add_to_cart' then 2 
-- when event_type ='purchase' then 3 
-- end as  step_number
-- from user_events
-- ),event_times as (
-- select user_id,
-- max(case when event_type='browse' then event_time end )as browse_time,
-- max(case when event_type='add_to_cart' then event_time end )as add_to_cart,
-- max(case when event_type='purchase' then event_time end )as purchase_time
-- from ordered_events
-- group by user_id 
-- )

-- select user_id,
-- case 
--     when browse_time is null then 'no bbrowse event'
--     when add_to_cart is null then 'dropped after browse event'
--     when purchase_time is null then 'dropped after add_to_cart'
--     else 'complered all funnel'
--     end as funnel_status,
-- TIMESTAMPdiff(minute,browse_time,add_to_Cart) as time_browse_to_Cart,
-- TIMESTAMPdiff(minute,add_to_Cart,purchase_time) as time_cart_to_purchase
-- from event_times


-- --  cohort _analysis
-- 1. 
-- with user_cohort as (
-- select distinct month(signup_date) from users 
-- )
-- ,
-- cohort_activty as(
-- select  u.user_id,  ue.event_time,
-- month(u.signup_date) as cohort_month,
-- TIMESTAMPdiff(month,u.signup_date,ue.event_time) as month_since_signup
-- from users u
-- join user_events ue  on ue.user_id=u.user_id
-- )

-- select cohort_month,month_since_signup,
-- count(distinct user_id) as active_users
-- from cohort_activty
-- group by cohort_month,month_since_signup











