from airflow.sdk import dag, task
from more_itertools import first

# Define the DAG using the decorator - function within function
@dag(
    dag_id="xcoms_dag_kwargs",
)
def xcoms_dag_kwargs():

    @task.python
    def first_task(**kwargs):

        #Extracting 'ti (task instance) from kwargs to push data to XCOMs
        ti = kwargs["ti"]

        print("Extracting Data.. This is the first task")
        fetched_date = {"data": [1, 2, 3, 4, 5]}
        ti.xcom_push(key="return_result", value=fetched_date)
    
    @task.python
    def second_task(**kwargs):
        #Extracting 'ti (task instance) from kwargs to pull data from XCOMs
        ti = kwargs["ti"]

        print("Transforming data... This is the second task")
        fetched_data = ti.xcom_pull(task_ids="first_task", key="return_result")["data"]
        transformed_data = [x * 2 for x in fetched_data]
        transformed_data = {"data": transformed_data}
        ti.xcom_push(key="return_result", value=transformed_data)
    
    @task.python
    def third_task(**kwargs):
        #Extracting 'ti (task instance) from kwargs to pull data from XCOMs
        ti = kwargs["ti"]
        load_data = ti.xcom_pull(task_ids="second_task", key="return_result")
        ti.xcom_push(key="return_result", value=load_data)

    # Define the task dependencies
    first = first_task()
    second = second_task()
    third = third_task()

    first >> second >> third 

# Instantiate the DAG
xcoms_dag_kwargs()
