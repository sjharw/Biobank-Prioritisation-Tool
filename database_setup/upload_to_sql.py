import sys
import pandas as pd
from configparser import ConfigParser
from sqlalchemy.exc import ProgrammingError
import pyodbc
import json
import numpy as np

# Set up path to root dir to access bespoke functions
config = ConfigParser()
config.read("config.ini")
ROOT = config["PATHS"]["root_dir"]

# import bespoke functions
if ROOT not in sys.path:
    sys.path.append(ROOT)

from functions.database import db_conn
from functions.utils import get_path_info, get_db_info

# Set up pathwasy and get database connection info
_, TEMP_DIR, _, DB_DIR, _, _ = get_path_info(config)
SERVER, USERNAME, PASSWORD, DRIVER, DB_NAME = get_db_info(config)

# Get metadata on dataframes
with open(DB_DIR + "metadata.json") as meta_file:
    metadata = json.load(meta_file)

##################################################
##-------- Connect to SQL & upload data --------##
##################################################

# Create SQL DB connection
engine = db_conn(
    driver=DRIVER,
    server=SERVER,
    database=DB_NAME,
    username=USERNAME,
    password=PASSWORD
    )

# Get names of dataframes (sources) and column names
df_names = [str(x) for x in metadata.keys()]  # ['iucn', 'cites', etc.]
col_names = [str(x['column_name']) for x in metadata.values()] # ['iucn_category', 'cites_listing', etc.]

# Read dataframes into list
suffix = '.parquet'
parquet_files = [s + suffix for s in df_names] # ['iucn.parquet', 'cites.parquet', etc.]
df_list = []
for file in parquet_files:
    df = pd.read_parquet(TEMP_DIR + file)
    df_list.append(df) 

# Zip name of df and df contents into a tuple
all_dfs = tuple(zip(df_names, df_list))

# Loop through the list of dataframe names and content and upload each one to SQL
for name, df in all_dfs:
    df.to_sql(name=name, con=engine, if_exists='replace', chunksize=20, method="multi", index=False)
    print(f"Uploaded {name} table to SQL.")

##################################################
##-------- Set Primary and Foreign keys --------##
##################################################

# Create list of column dtypes for each df
col_types = []
for df, cols in zip(df_list, col_names):
    subset = df[cols]
    col_types.append(subset.dtype)

# Map dtypes to SQL types
sql_type_map = {
    np.dtype('O'): 'VARCHAR(100)',
    np.dtype('float'): 'INTEGER',
    np.dtype('float32'): 'INTEGER',
    np.dtype('float64'): 'INTEGER',
    np.dtype('int'): 'INTEGER',
    np.dtype('int32'): 'INTEGER',
    np.dtype('int64'): 'INTEGER'
}

# Create list of SQL types for each column
sql_types = [sql_type_map.get(dt, dt) for dt in col_types]

# Create tuple of df names, column names, and column type
dfs_cols_tup = tuple(zip(df_names, col_names, sql_types)) # ((iucn', 'iucn_category'), ('cites', 'cites_listing'), etc.)

# Use tuple to create queries for each datasets to be uploaded to SQL
queries = []
for table, column, type in dfs_cols_tup:
    queries += [
        f"ALTER TABLE [{DB_NAME}].[dbo].{table} ALTER COLUMN full_name VARCHAR(100) NOT NULL;",
        f"ALTER TABLE [{DB_NAME}].[dbo].{table} ALTER COLUMN {column} {type};",
        f"ALTER TABLE [{DB_NAME}].[dbo].{table} ADD PRIMARY KEY (full_name);"
    ]

# Upload datasets to SQL using queries
with engine.connect() as conn:
    for query in queries:
        try:
            conn.execute(query)
        except ProgrammingError as e:
            if isinstance(e.orig, pyodbc.ProgrammingError) and 'primary key' in str(e.orig):
                raise Exception(f'Primary key already exists, process interrupted. {e.orig}')
            else:
                raise Exception(f'Something went wrong, process interrupted: {e}')