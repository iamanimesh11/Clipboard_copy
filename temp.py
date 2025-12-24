Below are two complete, practical examples of creating Glue tables directly in Athena (no crawler) — one for CSV and one for Parquet — both using partition projection.


---

✅ Example 1: CSV table (with partition projection)

S3 layout

s3://sales-bucket/sales_csv/
  year=2024/month=09/day=01/
    data.csv


---

Athena DDL (CSV)

CREATE EXTERNAL TABLE IF NOT EXISTS sales_csv (
  order_id      string,
  customer_id   string,
  amount        double,
  order_status  string
)
PARTITIONED BY (
  year  int,
  month int,
  day   int
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar'     = '"',
  'escapeChar'    = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://sales-bucket/sales_csv/'
TBLPROPERTIES (
  'skip.header.line.count' = '1',
  'projection.enabled' = 'true',

  'projection.year.type' = 'integer',
  'projection.year.range' = '2023,2026',

  'projection.month.type' = 'integer',
  'projection.month.range' = '1,12',
  'projection.month.digits' = '2',

  'projection.day.type' = 'integer',
  'projection.day.range' = '1,31',
  'projection.day.digits' = '2',

  'storage.location.template' =
    's3://sales-bucket/sales_csv/year=${year}/month=${month}/day=${day}/'
);


---

Query (CSV)

SELECT *
FROM sales_csv
WHERE year=2024 AND month=9 AND day=1;


---

✅ Example 2: Parquet table (with partition projection)

S3 layout

s3://sales-bucket/sales_parquet/
  year=2024/month=09/day=01/
    part-0001.parquet


---

Athena DDL (Parquet)

CREATE EXTERNAL TABLE IF NOT EXISTS sales_parquet (
  order_id      string,
  customer_id   string,
  amount        double,
  order_status  string
)
PARTITIONED BY (
  year  int,
  month int,
  day   int
)
STORED AS PARQUET
LOCATION 's3://sales-bucket/sales_parquet/'
TBLPROPERTIES (
  'projection.enabled' = 'true',

  'projection.year.type' = 'integer',
  'projection.year.range' = '2023,2026',

  'projection.month.type' = 'integer',
  'projection.month.range' = '1,12',
  'projection.month.digits' = '2',

  'projection.day.type' = 'integer',
  'projection.day.range' = '1,31',
  'projection.day.digits' = '2',

  'storage.location.template' =
    's3://sales-bucket/sales_parquet/year=${year}/month=${month}/day=${day}/'
);


---

Query (Parquet)

SELECT order_id, amount
FROM sales_parquet
WHERE year=2024 AND month=9 AND day=1;


---

🔍 CSV vs Parquet (important differences)

Aspect	CSV	Parquet

Storage	Large	Compact
Schema	Manual	Embedded
Performance	Slower	Faster
Cost	Higher	Lower
Serde needed	Yes	No



---

⚠️ Important notes

Do NOT run MSCK REPAIR TABLE

Always filter partition columns

Keep projection ranges tight

Schema must match data exactly



---

Interview one-liner 🧠

> CSV needs SerDe and header handling; Parquet is schema-aware and works best with partition projection.



If you want next:

Timestamp-based projection

JSON example

Schema evolution handling


Just tell me 👍