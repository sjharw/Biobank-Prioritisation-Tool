import json
import sys
from configparser import ConfigParser

# config
config = ConfigParser()
config.read("config.ini")
ROOT = config["PATHS"]["root_dir"]

# import bespoke functions
if ROOT not in sys.path:
    sys.path.append(ROOT)

from functions.utils import get_path_info
# import paths
_, _, _, DB_DIR, _, _ = get_path_info(config)

##--------- Create dictionary of score replacements
# dictionary of scores for each item
rep_dict = {
    "cites_listing": {
        "NC": 3,
        "I": 3,
        "I/NC": 3,
        "I/II": 2.5,
        "I/III": 2,
        "II": 2,
        "II/NC": 2,
        "II/III": 1.5,
        "III/NC": 1,
        "III": 1,
        "I/II/III/NC": 0,
        "I/II/NC": 0,
        "I/III/NC": 0,
        "II/III/NC": 0,
    },
    "iucn_category": {
        "EX": 1,
        "LC": 2,
        "LR/nt": 3,
        "LR/lc": 3,
        "LR/cd": 2,
        "DD": 4,
        "NT": 5,
        "VU": 6,
        "EN": 7,
        "EW": 8,
        "CR": 9,
    },
    "demand_scores" : {
        "Actinopterygii": 4,
        "Amphibia": 6,
        "Aves": 1,
        "Anthocerotopsida": 7,
        "Bryopsida": 9,
        "Chondrichthyes": 3,
        "Clitellata": 6,
        "Cycadopsida": 2,
        "Gastropoda": 2,
        "Ginkgoopsida": 1,
        "Insecta": 1,
        "Jungermanniopsida": 1,
        "Liliopsida": 3,
        "Magnoliopsida": 2,
        "Malacostraca": 1,
        "Mammalia": 6,
        "Marchantiopsida": 3,
        "Pinopsida": 3,
        "Reptilia": 2,
        "Sphagnopsida": 3,
        "Takakiopsida": 1,
    }
}
# create json object from dictionary
with open(DB_DIR + "scores.json", "w", encoding="utf8") as f:
    json.dump(rep_dict, f, ensure_ascii=False)


##--------- Create dictionary of dataset metadata
meta = {
    "iucn": {"column_name": "iucn_category"},
    "cites": {"column_name": "cites_listing"},
    "demand": {"column_name": "demand"},
    "edge": {"column_name": "ed_median"}
}
with open(DB_DIR + "metadata.json", "w") as f:
    json.dump(meta, f)
