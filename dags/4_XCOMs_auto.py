from airflow.sdk import dag, task
from more_itertools import first

# Define the DAG using the decorator - function within function
@dag(
    dag_id="xcoms_dag_auto",
)
def xcoms_dag_auto():

    @task.python
    def first_task():
        print("Extracting Data.. This is the first task")
        fetched_date = {"data": [1, 2, 3, 4, 5]}
        return fetched_date
    
    @task.python
    def second_task(data: dict):
        print("Transforming data... This is the second task")
        fetched_data = data["data"]
        transformed_data = [x * 2 for x in fetched_data]
        transformed_data = {"data": transformed_data}
        return transformed_data
    
    @task.python
    def third_task(data: dict):
        load_data = data
        return load_data

    # Define the task dependencies
    first = first_task()
    second = second_task(first)
    third = third_task(second)

    # first >> second >> third. It will automatically create the dag dependencies based on the function arguments and return values. This is called XCOMs in Airflow. It allows you to pass data between tasks without having to use a database or other external storage.

# Instantiate the DAG
xcoms_dag_auto()
