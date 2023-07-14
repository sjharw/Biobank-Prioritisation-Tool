##-- Libraries
from configparser import ConfigParser
import pandas as pd
import json
import sys
from sqlalchemy.engine import URL
from functools import reduce


##-- Setup

# Read config.ini
config = ConfigParser()
config.read("config.ini")
ROOT = config["PATHS"]["root_dir"]
if ROOT not in sys.path:
    sys.path.append(ROOT)

from functions.utils import get_db_info, get_path_info

# Get SQL connection information
SERVER, USERNAME, PASSWORD, DRIVER, DB_NAME = get_db_info(config)
# Get paths
_, TEMP_DIR, _, DB_DIR, _, _ = get_path_info(config)

# Get metadata
with open(DB_DIR + "metadata.json") as meta_file:
    metadata = json.load(meta_file)

##---------- Save temporary cache of dataset ----------##

# Get table names and column names from metadata
parquets = [str(x) + ".parquet" for x in metadata.keys()]  # ['iucn', 'cites', etc.]
col_names = [str(x['column_name']) for x in metadata.values()] # ['iucn_category', 'cites_listing', etc.]

# Read parquet tables into list
dfs = []
for col_name, parquet_name in zip(col_names, parquets):
    df = pd.read_parquet(TEMP_DIR + parquet_name)
    df = df[["full_name", "class", col_name]]
    dfs.append(df)

# Join the dataframes on full_name and class
merged_df = reduce(lambda left, right: pd.merge(left, right, on= ['full_name', 'class'], how='outer'), dfs)
# Drop duplicates, keeping first non-null value
merged_df = merged_df.groupby('full_name').first().sort_values("full_name").reset_index()


merged_df.to_parquet(TEMP_DIR + "entire_dataset.parquet", engine="fastparquet")

print("Database successfully create")