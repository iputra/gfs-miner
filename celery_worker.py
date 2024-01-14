from celery import Celery
app = Celery('my_tasks', broker='redis://localhost:6379/0')