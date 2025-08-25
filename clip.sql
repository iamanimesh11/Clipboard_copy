one thing i have noticed :when i create table normaly without partion by and cluster by clause then data got inserted into it successfully :
CREATE OR REPLACE TABLE Practice.ga_Sessions_partitioned_temp

but when i did CREATE OR REPLACE TABLE Practice.ga_Sessions_partitioned_temp2 PARTITION BY visit_date CLUSTER BY fullVisitorId,trafficsource as
  SELECT fullvisitorId,visitStartTime,totals.pageviews as pv,hits.page.pagePAth as pagePAth,trafficSource.source AS trafficsource,
          DATE(TIMESTAMP_SECONDS(visitStartTime)) as visit_date
  from   `bigquery-public-data.google_analytics_sample.ga_sessions_*`, UNNEST(hits) AS hits
  WHERE _TABLE_SUFFIX BETWEEN '20170801' AND '20170831';


table created as well but  problem is when i do  run
select count(*) from Practice.ga_Sessions_partitioned_temp2 ;

it SHOWS:This query will process 0 B when run.
BUT WHEN EXECUTED IT SHOWS COUNT AS :13233
