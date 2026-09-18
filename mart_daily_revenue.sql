CREATE OR REPLACE TABLE `learning-gcp-929.payflow_mart.daily_revenue` AS
SELECT 
    DATE(created_at) AS txn_date,
    currency,
    status,
    COUNT(*) AS txn_count,
    SUM(amount) AS total_amount
FROM `learning-gcp-929.payflow_raw.transactions`
GROUP BY status, txn_date, currency