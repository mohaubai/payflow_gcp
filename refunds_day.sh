#!/bin/bash

set -e
DAY=$1
PART=$(echo $DAY | tr -d '-')

#generate file
python3 gen_refunds.py $DAY

#upload the file into GCS
gcloud storage cp refunds_$DAY.csv gs://payflow_ubaid_09/refunds/raw/

#load into bq day partitioned using part
bq load --source_format=CSV --replace --skip_leading_rows=1 \
"learning-gcp-929:payflow_raw.refunds\$$PART" \
gs://payflow_ubaid_09/refunds/raw/refunds_$DAY.csv \
refund_id:STRING,txn_id:STRING,refund_amount:NUMERIC,refund_reason:STRING,created_at:TIMESTAMP

#update biquery marts dataset with daily_net_revenue table
bq query --use_legacy_sql=false < daily_net_revenue.sql