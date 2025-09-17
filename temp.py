WITH weekly_usage AS (
    SELECT 
        STR_TO_DATE(CONCAT(YEARWEEK(usage_date, 1), ' Monday'), '%X%V %W') AS week_start,
        COUNT(DISTINCT user_id) AS user_count
    FROM feature_usage
    WHERE feature_name = 'Smart Templates'
    GROUP BY YEARWEEK(usage_date, 1)
),

with_prev AS (
    SELECT 
        week_start,
        user_count,
        LAG(user_count) OVER (ORDER BY week_start) AS prev_count
    FROM weekly_usage
)

SELECT 
    week_start,
    user_count,
    CASE 
        WHEN prev_count IS NULL THEN NULL
        WHEN user_count >= prev_count * 1.5 THEN 'New Spike'
        WHEN user_count <= prev_count * 0.5 THEN 'Drop'
        ELSE 'Stable'
    END AS trend
FROM with_prev
ORDER BY week_start;