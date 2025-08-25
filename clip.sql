one thing i have noticed :when i create table normaly without partion by and cluster by clause then data got inserted into it successfully :
CREATE OR REPLACE TABLE Practice.ga_Sessions_partitioned_temp

but when i did CREATE OR REPLACE TABLE Practice.ga_Sessions_partitioned PARTITION BY visit_date CLUSTER BY fullVisitorId,trafficSource
table created as well but  problem is when i do  run
select * from Practice.ga_Sessions_partitioned  ;

it shows no data to display ,whats happening ,are you able to understand
