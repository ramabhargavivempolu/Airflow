from airflow.sdk import dag, task
from more_itertools import first

# Define the DAG using the decorator - function within function
@dag(
    dag_id="parallel_dag",
)
def parallel_dag():

    @task.python
    def extract_task(**kwargs):
        print("Extracting Data.. This is the first task")
        ti = kwargs["ti"]
        extacted_data_dict = {"api_extracted_data":[1,2,3,4,5],
                              "db_extracted_data":[6,7,8,9,10],

                              "s3_extracted_data":[11,12,13,14,15]}
        ti.xcom_push(key="return_value", value=extacted_data_dict)
    
    
    @task.python
    def transform_task_api(**kwargs):
        print("Transforming Data.. This is the second task")
        ti = kwargs["ti"]
        api_extracted_data = ti.xcom_pull(task_ids="extract_task", key="return_value")["api_extracted_data"]
        transformed_api_data = [x*10 for x in api_extracted_data]
        ti.xcom_push(key="return_value", value=transformed_api_data)
    
    @task.python
    def transform_task_db(**kwargs):
        print("Transforming Data.. This is the third task")
        ti = kwargs["ti"]
        db_extracted_data = ti.xcom_pull(task_ids="extract_task", key="return_value")["db_extracted_data"]
        transformed_db_data = [x*10 for x in db_extracted_data]
        ti.xcom_push(key="return_value", value=transformed_db_data)
    @task.python
    def transform_task_s3(**kwargs):
        print("Transforming Data.. This is the fourth task")
        ti = kwargs["ti"]
        s3_extracted_data = ti.xcom_pull(task_ids="extract_task", key="return_value")["s3_extracted_data"]
        transformed_s3_data = [x*10 for x in s3_extracted_data]
        ti.xcom_push(key="return_value", value=transformed_s3_data)

    @task.bash
    def load_task(**kwargs):
        print("Loading Data.. This is the fifth task")
        api_data = kwargs["ti"].xcom_pull(task_ids="transform_task_api", key="return_value")
        db_data = kwargs["ti"].xcom_pull(task_ids="transform_task_db", key="return_value")
        s3_data = kwargs["ti"].xcom_pull(task_ids="transform_task_s3", key="return_value")
        return "echo 'API Data: {} DB Data: {} S3 Data: {}'".format(api_data, db_data, s3_data)

    # Define the task dependencies
    extract = extract_task()
    transform_api = transform_task_api()
    transform_db = transform_task_db()
    transform_s3 = transform_task_s3()
    load = load_task()



    extract >> [transform_api, transform_db, transform_s3] >> load

# Instantiate the DAG
parallel_dag()