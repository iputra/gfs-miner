#!/usr/bin/python
import os

from datetime import datetime
from utils import read_yaml_config, generate_urls

# Path to your YAML file
base_path = os.path.abspath('')
config = read_yaml_config(f"{base_path}/config.yaml")

# Generate urls
filelist = generate_urls(
    datetime.strptime(config["initializer"]["start_date"], '%Y-%m-%d'),
    datetime.strptime(config["initializer"]["end_date"], '%Y-%m-%d'),
    config["initializer"]["release_hours"]
)