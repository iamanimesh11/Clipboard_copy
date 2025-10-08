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

