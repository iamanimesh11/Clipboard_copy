-- Step 1: Create a temp table to flatten hits
CREATE OR REPLACE TABLE Practice.ga_sessions_partitioned_temp AS
SELECT 
    fullVisitorId,
    visitStartTime,
    totals.pageviews AS pv,
    hits.page.pagePath AS pagePath,
    trafficSource.source AS trafficsource,
    DATE(TIMESTAMP_SECONDS(visitStartTime)) AS `visit_date`
FROM 
    `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
WHERE 
    _TABLE_SUFFIX BETWEEN '20170801' AND '20170831'
    AND visitStartTime IS NOT NULL;

-- Step 2: Create the partitioned & clustered table
CREATE OR REPLACE TABLE Practice.ga_sessions_partitioned
PARTITION BY `visit_date`
CLUSTER BY fullVisitorId, trafficsource AS
SELECT * FROM Practice.ga_sessions_partitioned_temp;

-- Step 3: Query the partitioned table (use DATE() for partition filter)
SELECT fullVisitorId, pv, trafficsource, pagePath, visit_date
FROM Practice.ga_sessions_partitioned
WHERE visit_date = DATE('2017-08-01')
LIMIT 10;

-- Step 4: Verify row counts
SELECT COUNT(*) AS total_rows, MIN(visit_date) AS min_date, MAX(visit_date) AS max_date
FROM Practice.ga_sessions_partitioned;