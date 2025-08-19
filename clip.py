CREATE OR REPLACE TABLE Practice.audit_log(

  visitor_id string,processed_at TIMESTAMP
)
CREATE OR REPLACE PROCEDURE Practice.log_visitors()
BEGIN 
  FOR cur in (
          SELECT fullvisitorid  from `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`
          GROUP BY fullvisitorid
          limit 5
  )
  DO 
    INSERT INTO Practice.audit_log(visitor_id,processed_at)  
    VALUES (cur.fullvisitorid,CURRENT_TIMESTAMP());

    END FOR;
    END;

CALL Practice.log_visitors()
