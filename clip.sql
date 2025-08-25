damn it . now i have made copied your code exactly and still its showing no data to display whne run select query:
CREATE OR REPLACE TABLE Practice.ga_Sessions_partitioned_temp as
  SELECT fullvisitorId,
          visitStartTime,
          totals.pageviews as pv,
          hits.page.pagePAth as pagePAth,
          trafficSource.source AS trafficsource,
          DATE(TIMESTAMP_SECONDS(visitStartTime)) as visit_date
  from   `bigquery-public-data.google_analytics_sample.ga_sessions_*`, UNNEST(hits) AS hits
  WHERE _TABLE_SUFFIX BETWEEN '20170801' AND '20170831' and visitStartTIme IS NOT NULL;


CREATE OR REPLACE TABLE Practice.ga_Sessions_partitioned PARTITION BY visit_date CLUSTER BY fullVisitorId,trafficsource as 
select * from Practice.ga_Sessions_partitioned_temp


select  fullvisitorId from Practice.ga_Sessions_partitioned
where visit_date='2017-08-01'
LIMIT 10;
