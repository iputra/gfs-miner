from celery_worker import app
import utils

@app.task
def process_file_task(url, file_path, latitude, longitude):
    result = utils.process_file(url, file_path, latitude, longitude)
    return result