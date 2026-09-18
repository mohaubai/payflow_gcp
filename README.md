# Payflow Project

[Generate CSV] -> [copy CSV to Google Cloud Storage] -> [Load the file into BigQuery table] --> [Update Mart]

We are using the file gen.py to generate CSV files with filename as transactions_YYYY-MM-DD.csv
This date in the file helps us load data into tables in a time partitioned method so that the pipeline stays idempotent and no duplicate gets created
The Google cloud storage path is gs://payflow_ubaid_09/raw
The bigquery Datasets are payflow_raw --> for raw data loaded directly payflow_mart --> business query

All this are wrrapped in a Airflow Dag Script which is stored in airflow/dags/payflow_dag.py

# Running It 
either using .sh file
./run_day.sh YYYY-MM-DD
or using airflow
airflow tasks test payflow_dag YYYY-MM-DD

## Marrkdown
Three questions. Answer each in a sentence or two, in your own words:

Why is the raw table partitioned by date, and why load with --replace into a single partition?
Why are raw and mart separate datasets?
Why explicit schemas instead of --autodetect?
1. Drop "project id." There's no project id involved. The partition key is the date from created_at. Say it like this:

The raw table is partitioned by date on created_at. Each day's file loads into only its own partition using --replace, so re-running the same day wipes and reloads just that slice. The load is idempotent — running it twice gives the same result as once, and no other day is touched.

2. Good, but add the consequence:

Raw is immutable — it stores exactly what the source sent. All casting and cleaning happen in the mart. That means the source data is still there to prove what arrived, even after a bug in the transformation.

3. Reframe it. Autodetect crashing would be fine — the real danger is it succeeding with the wrong type:

With autodetect, one dirty value makes BigQuery infer the whole column as STRING. That's what happened here: amount landed as STRING, silently. An explicit schema fails the load instead of quietly accepting bad types.

