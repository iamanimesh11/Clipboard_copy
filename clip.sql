-- Step 1: Create a brand new, temporary partitioned table
-- Note the new name `ga_sessions_partitioned_test`
CREATE OR REPLACE TABLE `Practice.ga_sessions_partitioned_test`
PARTITION BY visit_date
CLUSTER BY fullVisitorId, trafficsource AS
SELECT 
    fullVisitorId,
    visitStartTime,
    totals.pageviews AS pv,
    hits.page.pagePath AS pagePath,
    trafficSource.source AS trafficsource,
    DATE(TIMESTAMP_SECONDS(visitStartTime)) AS visit_date
FROM 
    `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
WHERE 
    _TABLE_SUFFIX BETWEEN '20170801' AND '20170831'
    AND visitStartTime IS NOT NULL;
    
-- Step 2: Immediately count the rows in the new table
SELECT COUNT(*) AS total_rows
FROM `Practice.ga_sessions_partitioned_test`;

-- Step 3: Immediately select from the new table
SELECT fullVisitorId, pv, trafficsource, pagePath, visit_date
FROM `Practice.ga_sessions_partitioned_test`
LIMIT 10;
