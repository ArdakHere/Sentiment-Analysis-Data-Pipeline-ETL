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

#TODO: Fix data inserting to BigQuery
    for _, row in csv_data.iterrows():
        row_data = {
            "news_string": row.get("news_string"),
            "publisher": row.get("publisher"),
            "sentiment": row.get("sentiment"),
            "color": row.get("color"),
            "timestamp": row.get("timestamp")
        }
        print(row_data)
        errors = bigquery_client.insert_rows_json(f"{project_id}.{dataset_id}.{table_id}", [row_data])
        if errors:
            print(f"Errors occurred while inserting rows: {errors}")

        # f"""
        # INSERT INTO {dataset_id}.{table_id} (news_string, publisher, sentiment, color, timestamp)
        # VALUES
        # ({row_data['news_string']}, {row_data['publisher']}, {row_data['sentiment']}, {row_data['color']}, {row_data['timestamp']});
        # """
        #
        # bigquery_client.query(query)
        

