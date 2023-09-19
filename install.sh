#!/bin/bash
set -e

source ~/miniconda3/etc/profile.d/conda.sh

# Setup Conda env
echo "Setting up Conda environment..."
# Create and activate conda environment
conda create --name priority-env python=3.10
conda activate priority-env
pip install -r requirements.txt
echo "Conda environment setup successfully"

echo "Please provide API keys to get app data"
# echo takes arguments that you pass to it through the command line
read -p "CITES API KEY: " cites_keyy
read -p "IUCN API KEY: " iucn_key

echo "ONLY AVAILABLE ON WINDOWS. Do you want to upload data to SQL? (y/n)"
read upload

if [ "$upload" = "y" ]; then
    # echo takes arguments that you pass to it through the command line
    read -p "SQL DRIVER: " db_driver
    read -p "SQL SERVER NAME: " db_server
    read -p "SQL DATABASE NAME: " db_name
    read -p "SQL USERNAME: " db_user
    read -p "SQL PASSWORD: " db_pass
    # Set up config.ini file
    python config_setup.py "$db_driver" "$db_server" "$db_name" "$db_user" "$db_pass" "$cites_key" "$iucn_key"
elif [ "$upload" = "n" ]; then
    # Set up config.ini file
    python config_setup.py "" "" "" "" "" "$cites_key" "$iucn_key"
else
    echo "Invalid choice for data upload. Please specify 'y' or 'n'."
    exit 1
fi

echo "Generating data for app..."
python database_setup/generate_metadata.py
python database_setup/taxonomy/generate_tax_rep.py
python database_setup/get_api_data.py
python database_setup/generate_dataframes.py
echo "Data created successfully"

if [ "$upload" = "y" ]; then
    echo "Uploading app data to SQL"
    python database_setup/upload_to_sql.py
    python database_setup/cache_sql_database.py
    python database_setup/generate_scored_dataset.py
elif [ "$upload" = "n" ]; then
    echo "Compiling app data"
    python database_setup/generate_entire_dataset.py
    python database_setup/generate_scored_dataset.py
else
    echo "Invalid choice for data upload. Please specify 'y' or 'n'."
    exit 1
fi

echo "Application has finished installing"
