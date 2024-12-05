from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
# sys.path.append('/opt/airflow/utils_shared')

from extract_and_load import extract_dag
from utils.transform_and_load import transform
from utils.load import load


with DAG(
    dag_id='news_dag',
    schedule=None,  # run manually
    tags=['python_school']
) as dag:
    extract_and_load_raw = PythonOperator(
        task_id='extract_and_load_op',
        python_callable=extract_dag,
        provide_context=True
    )
    transform_and_load = PythonOperator(  # Loads the transformed data into temp storage S3
        task_id='transform_and_load_op',
        python_callable=transform,
        provide_context=True
    )
    load_op = PythonOperator(  # Loads the transformed data from S3 into the database
        task_id='load_op',
        python_callable=load,
        provide_context=True
    )
    finish_op = EmptyOperator(
        task_id='finish'
    )

    extract_and_load_raw >> transform_and_load >> load_op >> finish_op
