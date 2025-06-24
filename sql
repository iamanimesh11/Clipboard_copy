🔥 PHASE 2: Business-Driven Aggregation – Customer Retention Analysis

🧠 Scenario:

You're working at a subscription-based fitness app (like Cult Fit or Fitbit). The CEO wants to understand user engagement and retention trends.
They've asked:

> “How many users make a repeat purchase within 30 days of their first one?
We want to improve retention. Give me insights.”

---

📦 Table: purchases

purchase_id	user_id	purchase_date
1	U1	2024-01-01
2	U1	2024-01-10
3	U1	2024-02-15
4	U2	2024-01-05
5	U2	2024-04-01
6	U3	2024-02-01
7	U3	2024-02-20
8	U4	2024-03-10



---

🎯 Task :

Find users who made a repeat purchase within 30 days of their first purchase

Return:
user_id,first_purchase_date,repeat_purchase_date (only the first one that qualifies)
Only one row per user who qualifies
Exclude users who never made a 2nd purchase within 30 days



---

🧠 Think Like This:

For each user:

Find their first purchase

Then look ahead for any next purchase within 30 days

Stop after the first valid repeat




---

Take your time. Think. Code. You already have the muscle — now show me retention insight power 📊

