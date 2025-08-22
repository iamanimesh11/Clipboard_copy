
-- PROCEDURE FOR LOOP ,CONDITIONALS AND DYNAMIC SQL
CREATE OR REPLACE PROCEDURE Practice.check_visitor_engagement(
  IN in_suffix string,
  IN low threshold INT64,
  IN high_threshold INT64,
  out out_Summary STRING 
  )
BEGIN 
 DECLARE sql STRING ;
 DECLARE fullvisitorid array;
 DECLARE pageviews array;

 SET sql= ''' SELECT fullvisitorid,totals.pageviews from `bigquery-public-data.google_analytics_sample.ga_sessions_*` where _TABLE_SUFFIX =@suffix ''';

 EXECUTE IMMEDIATE sql INTO fullvisitorid,pageviews USING in_suffix as suffix;

 select fullvisitorid,pageviews;
 

END;
