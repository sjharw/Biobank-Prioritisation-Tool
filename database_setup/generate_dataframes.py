###--- Library imports
import sys
import pandas as pd
import json
from configparser import ConfigParser

# config
config = ConfigParser()
config.read("config.ini")
ROOT = config["PATHS"]["root_dir"]

# import bespoke functions
if ROOT not in sys.path:
    sys.path.append(ROOT)

from functions.utils import get_path_info, nested_dicts_to_df, generate_demand, validate_df_schema, clean_dataframe

# import paths
_, TEMP_DIR, TAXON_DIR, DB_DIR, DS_DIR, _ = get_path_info(config)

###----- Required metadata and functions

## Taxonomic replacement dictionary
def load_tax_dicts():
    # Store filenames in a dictionary
    taxon_files = {
        "class": "class.json",
        "family": "family.json",
        "order": "order.json",
    }
    # Load JSON files and merge dictionaries
    tax_dicts = {}
    for taxon, filename in taxon_files.items():
        with open(TAXON_DIR + filename) as f:
            tax_dicts[taxon] = json.load(f)
    merged_dict = {**tax_dicts["class"], **tax_dicts["order"], **tax_dicts["family"]}
    return merged_dict

taxa_dict = load_tax_dicts()

## Demand score dictionary
with open(DB_DIR + "scores.json") as f:
    scores = json.load(f)
demand_scores = scores["demand_scores"]


##################################################
##--------- IUCN transform & clean ----------##
##################################################

## Import & transform
with open(TEMP_DIR + "iucn_response.json", "r") as f:
    iucn_dict = json.load(f)
iucn_df = nested_dicts_to_df(iucn_dict, "result")
iucn_df = iucn_df.rename(
    columns={"scientific_name": "full_name", "category": "iucn_category"}
)

# Clean
iucn = clean_dataframe(iucn_df, taxa_dict)

# Validate schema
iucn_schema = {
    'taxonid': int,
    'kingdom': str,
    'phylum': str,
    'class': str,
    'order': str,
    'family': str,
    'genus': str,
    'full_name': str,
    'taxonomic_authority': str,
    'infra_rank': str,
    'infra_name': str,
    'population': str,
    'iucn_category': str,
    'main_common_name': str
}

validate_df_schema(iucn, iucn_schema)

# Save cleaned datasets
iucn.to_parquet(TEMP_DIR + "iucn.parquet")

##################################################
##---------- CITES transform & clean ----------##
##################################################

with open(TEMP_DIR + "cites_response.json", "r") as f:
    cites_dict = json.load(f)

cites_df = pd.DataFrame.from_dict(cites_dict["taxon_concepts"])

#---- CITES common names df
dfs = [pd.DataFrame(sublist) for sublist in cites_df["common_names"]]
# Add the 'id' from the original dataset to each DataFrame
df_list = []
for sub_df in dfs:
    sub_df['id'] = cites_df['id']
    df_list.append(sub_df)
cn_df = pd.concat(df_list)

#---- CITES listings df
dfs = [pd.DataFrame(sublist) for sublist in cites_df["cites_listings"]]
listings_df = pd.concat(dfs)

#---- CITES synonyms df
dfs = [pd.DataFrame(sublist) for sublist in cites_df["synonyms"]]
synonyms_df = pd.concat(dfs)

#---- CITES df
# Append higher-taxa info to CITES df
tax = pd.DataFrame.from_records(cites_df["higher_taxa"])
cites_df = pd.concat([cites_df, tax], axis=1)
# Drop unwanted columns
cites_df.drop(
    ["higher_taxa", "common_names", "cites_listings", "synonyms"], axis=1, inplace=True
)

# Clean
cites_df = clean_dataframe(cites_df, taxa_dict)

# Validate schema
cites_schema = {
    'id': int,
    'full_name': str,
    'author_year': str,
    'rank': str,
    'name_status': str,
    'updated_at': str,
    'active': bool,
    'cites_listing': str,
    'kingdom': str,
    'phylum': str,
    'class': str,
    'order': str,
    'family': str
}

validate_df_schema(cites_df, cites_schema)

# Save
cites_df.to_parquet(TEMP_DIR + "cites.parquet")

##################################################
##---- Demand creation, transform & clean ----##
##################################################

# Generate demand data
demand_df = generate_demand(taxonomy_df=iucn, demand_scores=demand_scores)

# Validate schema
demand_schema = {
    'demand': float,
    'full_name': str,
    'class': str
}

validate_df_schema(demand_df, demand_schema)

demand_df.to_parquet(TEMP_DIR + "demand.parquet")


##################################################
##---------- EDGE transform & clean ----------##
##################################################

# Import & transforms
file = DS_DIR + "EDGE_List_2023.xlsx"
data = pd.ExcelFile(file)
# extract sheets of scores for non-plant species
score_sheets = [sheet for sheet in data.sheet_names if "score" in sheet and all(word not in sheet for word in ["corals", "gymnosperms"])]
# create df from list of sheets
df_list = []
for sheet in score_sheets:
    df = data.parse(sheet)
    df.columns = df.columns.str.lower()
    df_list.append(df)
# convert list of dfs to single concatinated df
edge_df = pd.concat(df_list)

# rename column names
edge_df.columns = edge_df.columns.str.replace('.', '_', regex=False)
edge_df.rename(columns={"species": "full_name"}, inplace=True)

# add class column 
edge_df["class"] = ""

# Clean
edge_df = clean_dataframe(edge_df, taxa_dict)

# Cast object columns to string columns
object_columns = edge_df.select_dtypes(include='object').columns
edge_df[object_columns] = edge_df[object_columns].astype('string')

# Validate schema
edge_schema = {
    'rl_id': float,
    'family': str,
    'full_name': str,
    'ed_median': float,
    'class': str
}
validate_df_schema(edge_df, edge_schema)

edge_df = edge_df[['rl_id', 'family', 'full_name', 'ed_median', 'class']]

# Save
edge_df.to_parquet(TEMP_DIR + "edge.parquet")