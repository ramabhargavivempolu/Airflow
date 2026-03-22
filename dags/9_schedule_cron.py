from airflow.sdk import dag, task
from pendulum import datetime
from airflow.timetables.trigger import CronTriggerTimetable


# Define the DAG using the decorator - function within function
@dag(
    dag_id="first_cron_dag",
    start_date=datetime(year=2024, month=3, day=21, tz="America/New_York"),
    schedule=CronTriggerTimetable("0 16 * * MON-FRI", timezone="America/New_York"),  # https://cron.help, https://crontab.guru/
    end_date=datetime(year=2024, month=3, day=29, tz="America/New_York"),
    is_paused_upon_creation=False,
    catchup=True
)
def first_cron_dag():

    @task.python
    def first_task():
        print("This is the first task")
    
    @task.python
    def second_task():
        print("This is the second task")
    
    @task.python
    def third_task():
        print("This is the third task")

    # Define the task dependencies
    first = first_task()
    second = second_task()
    third = third_task()

    first >> second >> third

# Instantiate the DAG
first_cron_dag()
