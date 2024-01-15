import os
import yaml

from sqlalchemy import create_engine, Column, Integer, String, Double, DateTime, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class GFS(Base):
    __tablename__ = 'gfs'
    id = Column(Integer, primary_key=True)
    release_hour = Column(String(100), nullable=False)
    datetime = Column(DateTime(timezone=True))
    rain = Column(Double)
    ws = Column(Double)
    temp = Column(Double)
    press = Column(Double)
    created_date = Column(TIMESTAMP, default=func.now())

# Path to your YAML file
def read_yaml_config(file_path):
    with open(file_path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
            return None

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = read_yaml_config(f"{base_path}/config.yaml")

# create an engine
engine = create_engine(config["gfs-miner"]["db"]["uri_connection"])

# create tables in the database
Base.metadata.create_all(engine)