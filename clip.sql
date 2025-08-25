I did this query as you said first create table then make another table(with partition by cluster by on that table_)but you see whats happening when i query my table 
  ga_Sessions_partitioned -its says no data to display and if same thing i do on ga_Sessions_partitioned_temp i.e select  fullvisitorId from Practice.ga_Sessions_partitioned_temp;
then it shows data ex expected,i dont know whats happening .pleas help

CREATE OR REPLACE TABLE Practice.ga_Sessions_partitioned_temp as
  SELECT fullvisitorId,
          visitStartTime,
          totals.pageviews as pv,
          hits.page.pagePAth as pagePAth,
          trafficSource.source AS trafficsource,
          DATE(TIMESTAMP_SECONDS(visitStartTime)) as visit_date
  from   `bigquery-public-data.google_analytics_sample.ga_sessions_*`, UNNEST(hits) AS hits
  WHERE _TABLE_SUFFIX BETWEEN '20170801' AND '20170831';



CREATE OR REPLACE TABLE Practice.ga_Sessions_partitioned PARTITION BY visit_Date CLUSTER BY fullVisitorId,trafficsource as 
select * from Practice.ga_Sessions_partitioned_temp


select  fullvisitorId from Practice.ga_Sessions_partitioned;
