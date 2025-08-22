CREATE OR REPLACE PROCEDURE Practice.sp_check_pageviews(IN in_suffix string ,IN  min_pageviews int64,out out_msg string)
BEGIN 

  DECLARE sql STRING;
  DECLARE n int64 default 0;
  SET sql='''
  SELECT count(totals.pageviews)  as count_pageViews from `bigquery-public-data.google_analytics_sample.ga_sessions_*` where _TABLE_SUFFIX =@suffix
''' ; 
  Execute IMMEDIATE SQL INTO n using in_suffix as suffix;
  if n =0 then 
  set out_msg="No data for this date";
  elseif n<min_pageviews then
    set out_msg=FORMAT("low activity:%d Pageviews",n);
  else 
    set out_msg=FORMAT("good traffic %d Pageviews",n);
  
  end if ;
END;

DECLARE nt string;
CALL  Practice.sp_check_pageviews('20170801',5,nt);
select nt;
