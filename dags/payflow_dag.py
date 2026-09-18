from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
import pendulum

default_args={
    "owner": "airflow",
    "email": ["mubaid675@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": pendulum.duration(minutes=2)
}

with DAG(
    dag_id="payflow_dag",
    schedule="@daily",
    start_date=pendulum.datetime(2026, 9, 18),
    catchup=False,
    default_args=default_args
) as dag:

    # #connect to gcp project
    # connect_gcp = BashOperator(
    #     task_id="connect_gcp",
    #     bash_command="gcloud config set project learning-gcp-929"
    # )

    #generate csv - python gen.py 2026-09-20
    generate_csv = BashOperator(
        task_id="generate_csv",
        bash_command="cd /home/mubaid675/gcp_project && python gen.py {{ ds }}"
    )

    #upload csv into GCP bucket
    upload_csv = BashOperator(
        task_id="upload_csv",
        bash_command="cd /home/mubaid675/gcp_project && gcloud storage cp transactions_{{ ds }}.csv gs://payflow_ubaid_09/raw/"
    )

    #load into Bigquery with partitioned date
    load_csv = BashOperator(
        task_id='load_csv',
        bash_command="""cd /home/mubaid675/gcp_project && bq load --source_format=CSV --replace --skip_leading_rows=1 \
                        'learning-gcp-929:payflow_raw.transactions${{ ds_nodash }}' \
                        gs://payflow_ubaid_09/raw/transactions_{{ ds  }}.csv \
                        txn_id:STRING,customer_id:STRING,amount:NUMERIC,currency:STRING,status:STRING,created_at:TIMESTAMP"""
    )

    #update mart table
    update_mart = BashOperator(
        task_id='update_mart',
        bash_command="cd /home/mubaid675/gcp_project && bq query --use_legacy_sql=false < mart_daily_revenue.sql"
    )

    #dependency
    generate_csv >> upload_csv >> load_csv >> update_mart