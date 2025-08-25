Below query doesnt show any data to display;

SELECT fullVisitorId FROM Practice.ga_Sessions_partitioned
WHERE visit_date = '2017-08-01'
LIMIT 10;


but when i query the main public dataset its shows output as expected .
SELECT 
    fullVisitorId
FROM 
    `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
WHERE 
    _TABLE_SUFFIX = '20170801';


i'm getting frustureated for real
