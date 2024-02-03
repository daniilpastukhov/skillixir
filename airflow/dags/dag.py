from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'my_parser_dag',
    default_args=default_args,
    description='A simple DAG to run my parser script',
    schedule_interval=timedelta(days=1),  # This schedules the DAG to run daily
    start_date=datetime(2024, 1, 1),  # Set an appropriate start date for your DAG
    catchup=False,  # If False, the DAG will only run for the latest interval if it has missed any runs
)

# Define the task
run_parser = BashOperator(
    task_id='run_my_parser',
    bash_command='python /path/to/your/parser_script.py ',  # Update the command to the path of your parser script
    dag=dag,
)

# Setting the task sequence (if you have multiple tasks)
# Here we only have one task, so this isn't necessary, but it's here for demonstration
run_parser
