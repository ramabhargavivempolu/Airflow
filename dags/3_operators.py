from airflow.sdk import dag, task
from airflow.operators.bash import BashOperator

# Define the DAG using the decorator - function within function
@dag(
    dag_id="operators_dag",
)
def operators_dag():

    @task.python
    def first_task():
        print("This is the first task")
    
    @task.python
    def second_task():
        print("This is the second task")
    
    @task.bash
    def bash_task_modern():
        return "echo https://airflow.apache.org/"
    
    bash_task_oldschool = BashOperator(
        task_id="bash_task_oldschool",
        bash_command="echo https://airflow.apache.org/"
    )

    # Define the task dependencies
    first = first_task()
    second = second_task()
    bash_task_modern = bash_task_modern()
    bash_task_oldschool = bash_task_oldschool

    first >> second >> bash_task_modern >> bash_task_oldschool

# Instantiate the DAG
operators_dag()
