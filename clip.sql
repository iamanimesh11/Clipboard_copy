from airflow import DAG
from airflow.operators.subdag import SubDagOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime

def create_subdag(parent_dag_id, child_dag_id, args):
    with DAG(dag_id=f"{parent_dag_id}.{child_dag_id}", default_args=args, schedule_interval=None) as subdag:
        t1 = DummyOperator(task_id="task_1")
        t2 = DummyOperator(task_id="task_2")
        t1 >> t2
    return subdag

args = {"start_date": datetime(2023,1,1)}

with DAG("subdag_example", default_args=args, schedule_interval=None) as dag:
    start = DummyOperator(task_id="start")

    subdag_task = SubDagOperator(
        task_id="child_dag",
        subdag=create_subdag("subdag_example", "child_dag", args),
    )

    end = DummyOperator(task_id="end")

    start >> subdag_task >> end
