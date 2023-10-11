# Sets up config.ini file
import os
from configparser import ConfigParser
import sys
import secrets
import datetime

# Create config parser object
config_object = ConfigParser()

# Access system arguments that were supplied to echo during install.bat installation
config_object["USER"] = {
    "SECRETKEY": secrets.token_hex(),
    "DATE": datetime.date.today().strftime('%d/%m/%Y')
    }

config_object["DATABASE"] = {
    "DRIVER": sys.argv[1],
    "SERVER_NAME": sys.argv[2],
    "DATABASE_NAME": sys.argv[3],
    "USERNAME": sys.argv[4],
    "PASSWORD": sys.argv[5],
}

config_object["API"] = {
    "CITES": sys.argv[6], 
    "IUCN": sys.argv[7]
}

# Set system pathways
root = os.path.dirname(os.path.abspath(__file__))
config_object["PATHS"] = {
    "ROOT_DIR": root,
    "TEMP_DIR": root + "/temp/",
    "DB_DIR": root + "/database_setup/",
    "TAXA_DIR": root + "/database_setup/taxonomy/",
    "DATASET_DIR": root + "/datasets/",
    "DOWNLOAD_DIR": root + "/downloaded/", 
}

# Write to config.ini
with open("config.ini", "w") as conf:
    config_object.write(conf)
