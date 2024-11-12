from datetime import datetime
from io import StringIO

import pandas as pd
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook

from google.cloud import bigquery

import boto3


def load(ti):
    """
    Load the processed data from S3 to BigQuery table

    Processed data is pulled from S3 using the URL stored in XCom
    """
    aws_conn_id = 'aws_connection'  # Use your connection ID
    conn = BaseHook.get_connection(aws_conn_id)

    aws_access_key_id = conn.login
    aws_secret_access_key = conn.password
    region_name = conn.extra_dejson.get('aws_region')

    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    bucket = ti.xcom_pull(key='bucket_name', task_ids='transform_and_load_op')
    key = ti.xcom_pull(key='key', task_ids='transform_and_load_op')
    current_date = ti.xcom_pull(key='today_date', task_ids='transform_and_load_op')
    response = s3_client.get_object(Bucket=bucket, Key=key)

    data = response['Body'].read().decode('utf-8')
    csv_data = pd.read_csv(StringIO(data))

    project_id = Variable.get("gcp_project_id")
    dataset_id = Variable.get("dataset_id")
    table_id = Variable.get("table_id")

    hook = BigQueryHook(gcp_conn_id="gc_connection")
    bigquery_client = hook.get_client()

    for _, row in csv_data.iterrows():
        row_data = {
            "news_string": row.get("news_string"),
            "publisher": row.get("publisher"),
            "sentiment": row.get("sentiment"),
            "color": row.get("color"),
            "sentiment_textual": row.get("sentiment_textual"),
            "timestamp": row.get("timestamp")
        }

        errors = bigquery_client.insert_rows_json(f"{project_id}.{dataset_id}.{table_id}", [row_data])
        if errors:
            print(f"Errors occurred while inserting rows: {errors}")


    # FREQUENCY LOADING
    bucket = ti.xcom_pull(key='bucket_name', task_ids='transform_and_load_op')
    key_freq = ti.xcom_pull(key='key_freq', task_ids='transform_and_load_op')
    current_date = ti.xcom_pull(key='today_date', task_ids='transform_and_load_op')
    response = s3_client.get_object(Bucket=bucket, Key=key_freq)

    data = response['Body'].read().decode('utf-8')
    csv_data = pd.read_csv(StringIO(data))

    project_id = Variable.get("gcp_project_id")
    dataset_id = Variable.get("dataset_id")
    table_id = Variable.get("table_id_freq")

    hook = BigQueryHook(gcp_conn_id="gc_connection")
    bigquery_client = hook.get_client()

    for _, row in csv_data.iterrows():
        row_data = {
            "word": row.get("word"),
            "count": row.get("count"),
            "timestamp": row.get("timestamp"),
        }

        errors = bigquery_client.insert_rows_json(f"{project_id}.{dataset_id}.{table_id}", [row_data])
        if errors:
            print(f"Errors occurred while inserting rows: {errors}")

