
-- BigQuery script example
BEGIN

  CREATE TEMP TABLE demo_table (
    totals STRUCT<pageviews INT64, transactions INT64>,
    tags ARRAY<STRING>,
    hits ARRAY<STRUCT<pagePath STRING, timeOnPage INT64>>
  );

  INSERT INTO demo_table (totals, tags, hits)
  VALUES
  (
    STRUCT(5 AS pageviews, 2 AS transactions),
    ['analytics', 'bigquery', 'demo'],
    [STRUCT('/home' AS pagePath, 10 AS timeOnPage),
     STRUCT('/about' AS pagePath, 5 AS timeOnPage)]
  ),
  (
    STRUCT(12 AS pageviews, 0 AS transactions),
    ['cloud', 'sql'],
    [STRUCT('/pricing' AS pagePath, 8 AS timeOnPage)]
  ),
  (
    STRUCT(0 AS pageviews, 0 AS transactions),
    [],  -- empty array
    []   -- empty array of structs
  );

  SELECT * FROM demo_table;

END;
