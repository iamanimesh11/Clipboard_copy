
-- 2. Behavioral Funnels:
-- For each user, sequence their events.]
-- Identify users who dropped off at each funnel step.
-- Compute time spent between steps.
WITH CTE AS(
select user_id,event_type,event_time,
case when event_type ='browse' then 1 
when event_type='add_to_cart' then 2 
when event_type ='purchase' then 3 
end as  rn ,

TIMESTAMPdiff(minute,lag(event_time) over (partition by user_id 
                order by field(event_type,'browse','add_to_cart','purchase')
),event_time ) as time_Diff
from user_events
)

SELECT user_id,
case when 1 not in (select rn where user_id=user_id) then 'browse',
case when 2 not in (select rn where user_id=user_id) then 'add_to_Cart',
case when 3 not in (select rn where user_id=user_id) then 'purchase'
end as c 
from cte 
