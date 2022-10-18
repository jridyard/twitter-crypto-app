from app.extensions import celery
from app.base.models import User
from time import sleep


@celery.task()
def basic_task(data):
    print("Waiting 5 seconds...")
    sleep(5)
    print("Task completed... 5 seconds later.")
    print(f"Your task id: { data['task_id'] }")