import os
from celery import Celery
from utils import read_yaml_config

base_path = os.path.abspath('')
config = read_yaml_config(f"{base_path}/config.yaml")

app = Celery('my_tasks', broker=config["gfs-miner"]["celery_broker_url"])