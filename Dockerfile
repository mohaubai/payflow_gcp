FROM google/cloud-sdk:slim
WORKDIR /app

COPY . .
RUN pip install dbt-bigquery --break-system-packages
RUN chmod +x run_day.sh
CMD ["sh", "-c", "./run_day.sh $DAY"]