WITH HourlyOrders AS (
    SELECT
        Customer_ID,
        HOUR(Order_Timestamp) AS Order_Hour,
        COUNT(*) AS Orders_Count
    FROM Orders
    GROUP BY Customer_ID, HOUR(Order_Timestamp)
),
RankedOrders AS (
    SELECT
        Customer_ID,
        Order_Hour,
        Orders_Count,
        ROW_NUMBER() OVER (
            PARTITION BY Customer_ID
            ORDER BY Orders_Count DESC, Order_Hour ASC
        ) AS rn
    FROM HourlyOrders
)
SELECT
    Customer_ID,
    Order_Hour AS Favourite_Hour,
    Orders_Count
FROM RankedOrders
WHERE rn = 1
ORDER BY Customer_ID;