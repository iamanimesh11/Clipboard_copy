
CREATE OR REPLACE PROCEDURE Practice.log_high_traffic_sessions(IN start_Date DATE,IN end_date DATE,OUT dates STRING)
BEGIN

 LOOP
 IF start_Date>end_Date then 
  BREAK;
 END IF; 
 
 set dates=","+string(start_Date);
 SET start_Date=DATE_ADD(start_Date,INTERVAL 1 DAY);

END LOOP;
END;

declare d string;
CALL Practice.log_high_traffic_sessions('2017-08-01','2017-08-05',d);
select d
