#!/bin/bash

set -e
DAY=$1
part = $(echo $DAY | tr -d '-')

#generate file
python3 gen_refunds.py $DAY

#upload the file into GCS
gcloud storage cp refunds_$DAY.csv gs://payflow_ubaid_09/refunds/raw/

#load into bq day partitioned using part
bq load --source_format=CSV --replace --skip_leading_rows=1 \
"learning-gcp-929:payflow_raw.refunds\$$PART" \
gs://payflow_ubaid_09/refunds/raw/refunds_$DAY.csv \
txn_id:STRING,customer_id:STRING,amount:NUMERIC,currency:STRING,created_at:TIMESTAMP



