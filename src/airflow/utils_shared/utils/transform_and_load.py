import boto3
import nltk
import pandas as pd
from airflow.hooks.base import BaseHook
from io import StringIO

from data_utils.data_processor import analyzer, assign_sentiment_color, assign_textual_sentiment, get_most_frequent_words

nltk.download('stopwords')


def transform(ti):
    """
    Transform the raw data by adding sentiment, color and timestamp columns

    Modify the DataFrame into .csv to simplify further analysis
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
    bucket = ti.xcom_pull(key='bucket_name', task_ids='extract_and_load_op')
    key = ti.xcom_pull(key='key', task_ids='extract_and_load_op')
    current_date = ti.xcom_pull(key='today_date', task_ids='extract_and_load_op')

    response = s3_client.get_object(Bucket=bucket, Key=key)

    data = response['Body'].read().decode('utf-8')

    raw_df = pd.read_csv(StringIO(data))

    raw_df = raw_df.melt(var_name="publisher", value_name="news_string")

    ### PROCESSING ###
    processed_df = pd.DataFrame(columns=['news_string', 'publisher', 'sentiment',
                                         'color', 'sentiment_textual', 'timestamp'])

    frequency_df = pd.DataFrame(columns=['word', 'count', 'timestamp'])

    raw_df.fillna('nan', inplace=True)

    for index, row in raw_df.iterrows():
        news_string = row['news_string']
        if news_string != 'nan':
            publisher = row['publisher']

            sentiment_index = analyzer.polarity_scores(news_string)

            sentiment_color = assign_sentiment_color(sentiment_index['compound'])
            sentiment_textual_index = assign_textual_sentiment(sentiment_index['compound'])

            processed_df = processed_df._append({
                'news_string': news_string,
                'publisher': publisher,
                'sentiment': sentiment_index['compound'],
                'sentiment_textual': sentiment_textual_index,
                'color': sentiment_color,
                'timestamp': current_date
            }, ignore_index=True)

    csv_buffer = StringIO()
    processed_df.to_csv(csv_buffer, index=False)

    bucket = 'news-bucket-etl'
    key = f'processed/processed_news_{current_date}.csv'
    s3_client.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
    s3_url = f"s3://{bucket}/{key}"

    ti.xcom_push(key='s3_url', value=s3_url)
    ti.xcom_push(key='key', value=key)
    ti.xcom_push(key='today_date', value=current_date)
    ti.xcom_push(key='bucket_name', value=bucket)

    freq_words_list = get_most_frequent_words(processed_df)

    for item in freq_words_list:
        frequency_df = frequency_df._append({
            'word': item[0],
            'count': item[1],
            'timestamp': current_date
        }, ignore_index=True)

    csv_buffer = StringIO()
    frequency_df.to_csv(csv_buffer, index=False)

    bucket = 'news-bucket-etl'
    key_freq = f'processed/frequency_words_{current_date}.csv'
    s3_client.put_object(Bucket=bucket, Key=key_freq, Body=csv_buffer.getvalue())
    print("Uploaded freq data")
    s3_url_freq = f"s3://{bucket}/{key_freq}"

    ti.xcom_push(key='s3_url_freq', value=s3_url_freq)
    ti.xcom_push(key='today_date', value=current_date)
    ti.xcom_push(key='key_freq', value=key_freq)
