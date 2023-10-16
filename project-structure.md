# Project structure

## Project Tree
```
.
|  .gitignore
|  app.py
|  config_setup.py
|  environment.yml
|  install.bat
|  README.md
|  setup.py
|              
|---database_setup
|  |  cache_sql_database.py
|  |  generate_dataframes.py
|  |  generate_entire_dataset.py
|  |  generate_metadata.py
|  |  generate_scored_dataset.py
|  |  get_api_data.py
|  |  metadata.json
|  |  scores.json
|  |  upload_to_sql.py
|  |  
|  |---taxonomy
|  |      generate_tax_rep.py
|  |      class.json
|  |      family.json
|  |      order.json
|  |  
|  |---schemas
|         cites_api.json
|         iucn_api.json
|          
|---datasets
|     cryoarks.csv
|     EDGE_Lists_2023.xlsx
|
|---downloaded
|      
|---functions
|     calculations.py
|     database.py
|     utils.py
|     __init__.py
|                 
|---static
|      custom.css
|      
|---temp
|      
|---templates
|      add.html
|      base.html
|      base_table.html
|      display.html
|      home.html
|      upload.html
|      
|---test
    |  test_api.py
    |  test_calculations.py
    |  test_read.py
    |  test_utils.py
    |  __init__.py
```

## Testing
 Bespoke functions in the '/functions' folder are tested with the `pytest` module. 
 
 You can run the tests from the Anaconda prompt:
 - Change the path to point at the project directory: `cd path/to/project/folder`
 - Run the tests: `pytest test/*.py`

## Folders and files
**Database setup**
<br>
There is a folder called '/database_setup' that contains the scripts required to create the scored dataset. The scored dataset is the data displayed on the display page, without the scored_dataset.parquet file, the application will fail to load correctly.
The data is either retrieved from APIs (IUCN and CITES), generated (demand), or read in from csv/ xlsx files (EDGE, CryoArks).
<br>
<br>
Below is a list of datasources ingested or created when '/database_setup' is run:

- [IUCN API](https://apiv3.iucnredlist.org/about)
- [Species+/CITES Checklist API](https://api.speciesplus.net/documentation)
- [EDGE](https://www.edgeofexistence.org/edge-lists/) (xlsx file)
- Demand (fake data that is generated)
- [CryoArks](https://www.cryoarks.org/) (csv file)

The Extract Transform (Load) pipeline, for creating the data required for the app to run, can be broken down into the following scripts that are all contained within 'database_setup' folder:

- `get_api_data.py`: retrieves API data for IUCN and CITES
- `generate_dataframes.py`: cleans and transforms IUCN, CITES and EDGE data, generates demand data
- `generate_entire_dataset.py`: compiles all dataframes into single dataset
- `upload_to_sql.py`: uploads cleaned dataframes to SQL as tables
- `cache_database.py`: caches datasets from SQL as a single compiled dataset
- `generate_scored_dataset.py`: uses compiled dataset to generate a parquet containing species score data required for app to run

Depending on which option you choose at installation (SQL), certain files will be run from the 'database_setup' folder


These scripts rely on several JSON files located in the root directory of the 'database_setup' folder or within subfolders in the 'database_setup' folder.
Within the root of 'database_setup' folder there is a `generate_metadata.py` file that creates two JSON files used by the `cache_scored_data.py` script:
- `scores.json`: dictionary of scores used to convert non-numeric IUCN and CITES data to numeric, and dictionary of means for each class of species used to generate fake demand data.
- `metadata.json`: dictionary of SQL table names and column names to be cached.

The `/taxonomy` subfolder contains a python script called `generate_tax_rep.py` that generates json files of dictionaries of common taxonomic errors. These JSON files are are used to replace any possible taxonomic data errors during the cleaning stage of the pipeline. The `schemas` subfolder contains JSON files of the expected IUCN and CITES schemas that are used to validate the schema of the JSON results from the API requests.

### Temp
API request responses, intermediate tables, and cached data are all saved to the /temp folder. Do not delete this folder, it contains the data required for the app to run.

## Datasets
The /datasets folder contains the CryoArks dataset and EDGE 2023 dataset.

## Downloaded
The /downloaded folder is where downloads from the application are saved to.