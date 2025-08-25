getting error:Cannot access field source on a value with type STRING at [1:150]

CREATE OR REPLACE TABLE Practice.ga_Sessions_partitioned PARTITION BY DATE(TIMESTAMP_SECONDS(visitStartTime)) CLUSTER BY fullVisitorId,trafficSource.source
AS 
  SELECT fullvisitorId,
          visitStartTime,
          totals.pageviews,
          hits.page.pagePAth as pagePAth,
          trafficSource.source AS trafficsource
  from   `bigquery-public-data.google_analytics_sample.ga_sessions_*`, UNNEST(hits) AS hits
  WHERE _TABLE_SUFFIX BETWEEN '20170801' AND '20170831';
