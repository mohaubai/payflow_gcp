CREATE OR REPLACE TABLE `learning-gcp-929.payflow_mart.daily_net_revenue` AS

WITH daily_transactions AS (
    SELECT
        DATE(created_at) AS txn_date,
        SUM(amount) AS gross_amount
    FROM `learning-gcp-929.payflow_raw.transactions`
    WHERE status = 'approved'
    GROUP BY txn_date
),

daily_refunds AS (
    SELECT
        DATE(t.created_at) AS txn_date,
        SUM(r.refund_amount) AS refund_amount
    FROM `learning-gcp-929.payflow_raw.refunds` r
    JOIN `learning-gcp-929.payflow_raw.transactions` t
        ON r.txn_id = t.txn_id
        AND DATE(r.created_at) = DATE(t.created_at)
    WHERE t.status = 'approved'
    GROUP BY txn_date
)

SELECT
    t.txn_date,
    t.gross_amount,
    COALESCE(r.refund_amount, 0) AS refund_amount,
    t.gross_amount - COALESCE(r.refund_amount, 0) AS net_amount,
    SAFE_DIVIDE(
        COALESCE(r.refund_amount, 0),
        t.gross_amount
    ) * 100 AS refund_rate

FROM daily_transactions t
INNER JOIN daily_refunds r
    ON t.txn_date = r.txn_date
ORDER BY t.txn_date;