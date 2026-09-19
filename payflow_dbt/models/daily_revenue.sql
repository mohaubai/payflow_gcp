{{ config(materialized='table') }}

SELECT 
    DATE(created_at) AS txn_date,
    currency,
    status,
    COUNT(*) AS txn_count,
    SUM(amount) AS total_amount
FROM {{ source('payflow_raw', 'transactions') }}
GROUP BY status, txn_date, currency