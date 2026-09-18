#!/bin/bash 
set -e
DAY=$1
PART=$(echo $DAY | tr -d '-')

#1. generate
python gen.py $DAY

#2. upload
gcloud storage cp transactions_$DAY.csv gs://payflow_ubaid_09/raw/

#3. load into partition
bq load --source_format=CSV --replace --skip_leading_rows=1 \
"learning-gcp-929:payflow_raw.transactions\$$PART" \
gs://payflow_ubaid_09/raw/transactions_$DAY.csv \
txn_id:STRING,customer_id:STRING,amount:NUMERIC,currency:STRING,status:STRING,created_at:TIMESTAMP

#4. rebuild mart
bq query --use_legacy_sql=false < mart_daily_revenue.sql