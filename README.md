# GFS-Miner
GFS Miner is a tool for extracting historical climate data from [NOAA GFS (Global Forecast System)](https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast), available on the [UCAR (University Corporation for Atmospheric Research)](https://rda.ucar.edu/datasets/ds084.1/dataaccess/) website. This powerful tool utilizes distributed tasks through Redis and Celery in Python, ensuring lightning-fast downloads and processing of the data.

## Install Requirements

```
sudo apt update
sudo apt install -y gcc make python3-dev python3-venv libmariadb-dev

pip3 install -r requirements.txt
```
