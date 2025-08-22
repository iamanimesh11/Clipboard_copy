
-- PROCEDURE FOR LOOP ,CONDITIONALS AND DYNAMIC SQL
CREATE OR REPLACE PROCEDURE Practice.check_visitor_engagement(
  IN in_suffix string,
  IN low_threshold INT64,
  IN high_threshold INT64,
  out out_Summary STRING 
  )
BEGIN 
 DECLARE sql STRING ;
 DECLARE visitor STRING ;
 DECLARE pageviews int64 ;
 DECLARE summary STRING DEFAULT '';
 DECLARE low_count INT64 DEFAULT 0;
 DECLARE medium_count INT64 DEFAULT 0;
 DECLARE high_count INT64 DEFAULT 0;

 SET sql= ''' CREATE TEMP TABLE tmp As
          SELECT
               fullvisitorid,totals.pageviews as pageviews from `bigquery-public-data.google_analytics_sample.ga_sessions_*` where _TABLE_SUFFIX =@suffix LIMIT 500 '''; 

   EXECUTE IMMEDIATE sql USING in_suffix AS suffix;          

for record IN (SELECT fullvisitorid,pageviews from tmp)
DO
  set visitor =record.fullVIsitorID;
  set pageviews=record.pageviews;

  if pageviews<low_threshold then 
    set summary= format('Visitor %s is LOW- %d ',visitor,pageviews );
    SET low_count=low_count+1;
  elseif pageviews >= low_threshold and pageviews<high_threshold then
      SET medium_count=medium_count+1;
      set summary= format('Visitor %s is Medium- %d ',visitor,pageviews );

  else 
        SET high_count=high_count+1;
        SET  summary= format('Visitor %s is HIGH - %d ',visitor,pageviews );
  END IF;
END FOR;

SET out_summary=FORMAT("Low: %d, Medium: %d, High: %d",low_count,medium_count,high_count);

END;

declare t  string;
call  Practice.check_visitor_engagement('20170801',2,5,t);
select t;
