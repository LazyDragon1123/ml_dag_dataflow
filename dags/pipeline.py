from datetime import datetime, timedelta

from airflow.decorators import dag, task
from manage_data.extract import extract
from manage_data.generate import create_receipt
from manage_data.save import push_total

default_args = {
    "owner": "yuki",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1, 0, 0, 0),
    "schedule": timedelta(days=1),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


@dag(default_args=default_args)
def ml_task():
    @task()
    def receive_data():
        create_receipt()
        return True

    @task(multiple_outputs=True)
    def parse(is_received: bool):
        res = {}
        if is_received:
            res = extract()
        if bool(res):
            return {"total_values": extract()}
        else:
            return {"total_values": {}}

    @task()
    def push_analytics(total_values):
        if bool(total_values):
            push_total(total_values)

    is_received = receive_data()
    parsed = parse(is_received)
    push_analytics(parsed["total_values"])


dag = ml_task()
