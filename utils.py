import yaml
from datetime import timedelta

def read_yaml_config(file_path):
    with open(file_path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
            return None

def generate_urls(start_date, end_date, release_hours):
    urls = []
    current_date = start_date
    while current_date <= end_date:
        for release_hour in release_hours:
            for f in range(0, 120, 3):
                year = current_date.strftime("%Y")
                month = current_date.strftime("%m")
                date = current_date.strftime("%d")
                urls.append(f"https://data.rda.ucar.edu/ds084.1/{year}/{year}{month}{date}/gfs.0p25.{year}{month}{date}{release_hour}.f{f:03d}.grib2")
        current_date += timedelta(days=1)
    
    return urls