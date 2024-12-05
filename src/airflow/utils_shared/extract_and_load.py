import logging
from datetime import datetime
from io import StringIO

import boto3
import pandas as pd
from airflow.hooks.base import BaseHook
from botocore.exceptions import ClientError, BotoCoreError

from data_utils.ingest_aggregator import extract_webscraped_strings


def extract_dag(ti):
    """
    Webscrape news strings and ingest them into a DataFrame
    """

    news_data_combined = extract_webscraped_strings()

    try:
        raw_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in news_data_combined.items()]))
        pd.set_option('display.max_columns', None)
    except Exception as e:
        logging.error(f"Failed to create DataFrame: {e}")
        raise

    try:
        aws_conn_id = 'aws_connection'  # Use your connection ID
        conn = BaseHook.get_connection(aws_conn_id)
    except Exception as e:
        logging.error(f"Failed to establish AWS connection: {e}")
        raise

    try:
        aws_access_key_id = conn.login
        aws_secret_access_key = conn.password
        region_name = conn.extra_dejson.get('aws_region')
    except Exception as e:
        logging.error(f"Failed to get AWS credentials: {e}")
        raise

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
    except Exception as e:
        logging.error(f"Failed to create S3 client with given AWS credentials: {e}")
        raise

    csv_buffer = StringIO()
    raw_df.to_csv(csv_buffer, index=False)

    today = datetime.today().date()

    bucket = 'news-bucket-etl'
    key = f'raw/raw_news_{today}.csv'

    try:
        s3_client.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
    except (BotoCoreError, ClientError) as e:
        print(f"An error occurred with S3: {e}, while uploading to {bucket}/{key}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}, while uploading to {bucket}/{key}")
        raise

    s3_url = f"s3://{bucket}/{key}"

    ti.xcom_push(key='s3_url', value=s3_url)
    ti.xcom_push(key='today_date', value=today)
    ti.xcom_push(key='bucket_name', value=bucket)
    ti.xcom_push(key='key', value=key)

