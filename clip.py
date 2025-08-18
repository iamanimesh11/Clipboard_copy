pCREATE OR REPLACE PROCEDURE my_dataset.process_users()
BEGIN
  DECLARE done BOOL DEFAULT FALSE;
  DECLARE v_user_id INT64;
  DECLARE v_user_name STRING;

  -- Define a cursor for selecting users
  DECLARE user_cursor CURSOR FOR
    SELECT user_id, user_name
    FROM my_dataset.users;

  -- Open cursor and iterate row by row
  OPEN user_cursor;

  user_loop:
  LOOP
    FETCH user_cursor INTO v_user_id, v_user_name;
    IF done THEN
      LEAVE user_loop;
    END IF;

    -- Example processing: Insert into a log table
    INSERT INTO my_dataset.user_log (log_time, message)
    VALUES (CURRENT_TIMESTAMP(), CONCAT("Processed user: ", v_user_name));

  END LOOP;

  CLOSE user_cursor;
END;
