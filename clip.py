

CREATE OR REPLACE PROCEDURE Practice.top_pages(in_suffix String,out page_count int64)
BEGIN
  DECLARE sql STRING;
  SET sql='''
    SELECT count(*) from (
      SELECT h.page.pagePath from `bigquery-public-data.google_analytics_sample.ga_sessions_*`,unnest(hits) h 
    where _TABLE_SUFFIX= @suffix and h.type='PAGE'
    )
    ''';

EXECUTE IMMEDIATE sql USING suffix AS in_suffix INTO page_count;
END;
