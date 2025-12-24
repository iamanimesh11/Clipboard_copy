Great — STEP 9: Advanced Transformations in Glue is where your ETL pipeline starts behaving like a real production system.

Up to now, you did:

Raw CSV → Parquet (Processed Layer)

Parquet → Curated (with simple transformations)


Now we go deeper into actual enterprise-grade Glue ETL transformations:

🚀 What You’ll Learn in STEP 9

These are MUST-HAVE skills for a data engineer:

Joining multiple datasets

Filtering, cleaning, removing duplicates

Handling nulls & data quality

Aggregations

Derived/Calculated fields

Window functions (advanced Spark concept)

Writing partitioned Parquet output


We’ll do hands-on examples using Glue (Spark).
Everything will be demonstrated with your sales dataset.


---

🔥 STEP 9.1 — Add Another Dataset to Join With

In real data pipelines, data rarely exists alone.

Let's create a new dataset:

Customer Details

Make a new CSV:

id,city,age
1,Delhi,26
2,Pune,28

Upload it to:

s3://my-de-lake-animesh11/customers/

Then create a crawler:

customers-crawler

Source:
s3://my-de-lake-animesh11/customers/

Database:
sales_demo_db

This creates a table:

customers

Now we can join sales + customers in Glue ETL.


---

🚀 STEP 9.2 — Create an Advanced Glue Job

Create a new Glue Job:

sales_transform_advanced

Select Script editor (so we can manually write code).


---

🧠 STEP 9.3 — Perform Real Transformations (JOIN + CLEAN + AGGREGATION)

Paste this script:

import sys
from pyspark.sql import functions as F
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 🔹 Read sales parquet (processed layer)
sales_df = spark.read.parquet("s3://my-de-lake-animesh11/sales_parquet/")

# 🔹 Read customer dataset
cust_df = spark.read.option("header", "true").csv("s3://my-de-lake-animesh11/customers/")

# Convert types
cust_df = cust_df.withColumn("id", F.col("id").cast("int")) \
                 .withColumn("age", F.col("age").cast("int"))

# 🔹 JOIN datasets
joined = sales_df.join(cust_df, "id", "left")

# 🔹 CLEANING: Replace nulls
cleaned = joined.fillna({"city": "Unknown", "age": 0})

# 🔹 DERIVED COLUMNS
final_df = cleaned.withColumn("name_upper", F.upper(F.col("name"))) \
                  .withColumn("sales_tax", F.col("sales") * 0.18) \
                  .withColumn("total_sales", F.col("sales") + F.col("sales") * 0.18)

# 🔹 AGGREGATION: Sales by city
agg_df = final_df.groupBy("city").agg(
    F.sum("sales").alias("total_city_sales"),
    F.count("*").alias("num_customers")
)

# Write curated outputs
final_df.write.mode("overwrite").parquet("s3://my-de-lake-animesh11/sales_curated/")
agg_df.write.mode("overwrite").parquet("s3://my-de-lake-animesh11/sales_city_summary/")

job.commit()


---

🔥 What This Script Actually Does (Clear Explanation)

1️⃣ Read processed sales data

Your Parquet data.

2️⃣ Read customer data

The new CSV dataset.

3️⃣ Join on id

This simulates a real star-schema or fact-dimension join.

4️⃣ Clean data

Replace NULLs.

5️⃣ Create new business columns

uppercase name

sales tax

total sales


6️⃣ Aggregation

Generates:

sales by city
number of customers per city

7️⃣ Writes TWO curated outputs

sales_curated (clean + enriched)

sales_city_summary (aggregated insight)


This is EXACTLY how real enterprise ETL runs.


---

🧪 STEP 9.4 — Crawler for Summary/Curated Tables

Create a crawler for:

s3://my-de-lake-animesh11/sales_city_summary/

This creates:

sales_city_summary


---

🧪 STEP 9.5 — Query in Athena

Query 1 — Joined + Cleaned + Enriched Table:

SELECT id, name_upper, city, sales, total_sales
FROM sales_curated;

Query 2 — Aggregated Summary:

SELECT * FROM sales_city_summary;

Expected:

city	total_city_sales	num_customers

Delhi	5000	1
Pune	6000	1



---

🎉 You Now Performed Real ETL Transformations

✔ Join
✔ Cast types
✔ Clean/replace nulls
✔ Derived metrics
✔ Aggregation
✔ Multiple output datasets
✔ Updated curated architecture

This is REAL data engineering work — the stuff done in production systems.


---

⭐ Next Step Options

NEXT → Step 10: Athena Performance Tuning (Partition pruning, compression, column selection)

Or Step 10B: Glue Job Best Practices (parallelism, repartitioning, broadcast joins)

Or Step 10C: Workflow Automation (Glue Workflows + EventBridge triggers)

Tell me:

“Step 10”
or
“Glue performance”
or
“Automation next”

Your choice!