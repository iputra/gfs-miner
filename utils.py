import os
import yaml
import requests
import re
import xarray
import pandas as pd
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

def download_file(url, destination_path):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(destination_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return f"Downloaded file from {url} to {destination_path}"
    else:
        return f"Failed to download file from {url}, status code: {response.status_code}"

def remove_file(file_path):
    if os.path.exists(file_path):
    # Remove the file
        os.remove(file_path)
        print(f"File removed successfully {file_path}.")
    else:
        print(f"The file {file_path} does not exist.")

def get_datetime(file_path, is_first):
    if is_first:
        ds = xarray.open_dataset(file_path, filter_by_keys={'typeOfLevel': 'surface'})
    else:
        ds = xarray.open_dataset(file_path, filter_by_keys={'stepType': 'instant', 'typeOfLevel': 'surface'})
    
    return ds.valid_time.values

def slice_data(file_path, latitude, longitude, var, is_first):
    if is_first and var == "tp":
        return 0
    elif is_first:
        ds = xarray.open_dataset(file_path, filter_by_keys={'typeOfLevel': 'surface'}, engine="cfgrib")
    elif var == "tp":
        ds = xarray.open_dataset(file_path, filter_by_keys={'stepType': 'accum', 'typeOfLevel': 'surface'}, engine="cfgrib")
    else:
        ds = xarray.open_dataset(file_path, filter_by_keys={'stepType': 'instant', 'typeOfLevel': 'surface'}, engine="cfgrib")
    
    return float(ds[var].sel(latitude=latitude, longitude=longitude, method="nearest").values)

def get_release_hour(file_path):
    match = re.search(r'\d{10}', file_path).group()
    return match

def insert_data(url, data):

    payload = {
        "release_hour": data["release_hour"],
        "datetime": str(data["Datetime"]),
        "rain": data["rain"],
        "ws": data["ws"],
        "temp": data["temp"],
        "press": data["press"]
    }
    headers = {"content-type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    return response.json()

def process_file(url, file_path, latitude, longitude):
    base_path = os.path.abspath('')
    config = read_yaml_config(f"{base_path}/config.yaml")
    
    download_file(url, file_path)
    
    # check first forecast or not
    forecast_hour = re.search(r'f\d{3}', file_path).group()
    is_first = True if forecast_hour == "f000" else False

    # get datetime
    valid_time = get_datetime(file_path, is_first)

    # get release hour
    release_hour = get_release_hour(file_path)
    
    # rain (tp)
    rain = slice_data(file_path, latitude, longitude, "tp", is_first)
    
    # wind speed (gust)
    ws = slice_data(file_path, latitude, longitude, "gust", is_first)
    
    # temperature (t)
    temp = slice_data(file_path, latitude, longitude, "t", is_first)
    
    # pressure (sp)
    press = slice_data(file_path, latitude, longitude, "sp", is_first)
    
    # add data to dataframe
    row = {
           'release_hour': release_hour,
           'Datetime': valid_time, 
           'rain': rain, 
           'ws': ws, 
           'temp': temp, 
           'press': press}

    # store data to pocketbase
    insert_data(config["api_store"]["url"], row)
    
    # remove file
    remove_file(file_path)

    return row