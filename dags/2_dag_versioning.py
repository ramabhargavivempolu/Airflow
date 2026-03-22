from airflow.sdk import dag, task
from more_itertools import first

# Define the DAG using the decorator - function within function
@dag(
    dag_id="versioned_dag",
)
def versioning_dag():

    @task.python
    def first_task():
        print("This is the first task")
    
    @task.python
    def second_task():
        print("This is the second task")
    
    @task.python
    def third_task():
        print("This is the third task")
    
    @task.python
    def version_task():
        print("This is the version task")

    # Define the task dependencies
    first = first_task()
    second = second_task()
    third = third_task()
    version = version_task()

    first >> second >> third >> version

# Instantiate the DAG
versioning_dag()
