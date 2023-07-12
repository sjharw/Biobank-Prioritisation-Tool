##-- Libraries
from configparser import ConfigParser
import pandas as pd
import sys
import warnings
import json

# Get paths from config file
config = ConfigParser()
config.read("config.ini")
ROOT = config["PATHS"]["root_dir"]
if ROOT not in sys.path:
    sys.path.append(ROOT)

from functions.utils import get_path_info
from functions.calculations import Calculations, enforce_float

_, TEMP_DIR, _, DB_DIR, _, _ = get_path_info(config)

##------------ Create scored dataset ---------##

data = pd.read_parquet(TEMP_DIR + "entire_dataset.parquet")

with open(DB_DIR + "metadata.json") as meta_file, open(DB_DIR + "scores.json") as scores_file:
    metadata = json.load(meta_file)
    scores = json.load(scores_file)

# Create column of % of null values across data sources (iucn, cites, edge, demand)
metacols = [m["column_name"] for m in metadata.values()]
data["null_percent"] = (data[metacols].isna().sum(axis=1) / len(metacols)) * 100
data["null_percent"] = (data["null_percent"]).astype(int)

# Score data and ensure scored data is float type
data = data.replace(scores)
data[metacols] = data[metacols].apply(enforce_float)

# Rescale data
for col in metacols:
    if col in data.columns:
        # pass series through calculations class
        calc = Calculations(data[col])
        data[col] = calc.divide_max()
    else:
        # warn user if column is missing from metadata
        warnings.warn(f"{col} is not in {data.columns}")

# save scored/ scaled data
data.to_parquet(TEMP_DIR + "scored_dataset.parquet")

print("Scored dataset successfully created")