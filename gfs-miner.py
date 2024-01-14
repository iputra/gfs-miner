#!/usr/bin/python
import os

from datetime import datetime
from utils import read_yaml_config, generate_urls

# Path to your YAML file
base_path = os.path.abspath('')
config = read_yaml_config(f"{base_path}/config.yaml")

# Generate urls
urls = generate_urls(
    datetime.strptime(config["gfs-miner"]["start_date"], '%Y-%m-%d'),
    datetime.strptime(config["gfs-miner"]["end_date"], '%Y-%m-%d'),
    config["gfs-miner"]["release_hours"]
)

# Put to queue
from tasks import process_file_task

for url in urls:
    result = process_file_task.delay(url,
                                     config["gfs-miner"]["output_dir"] + os.path.basename(url),
                                     config["gfs-miner"]["latitude"],
                                     config["gfs-miner"]["longitude"]
                                     )