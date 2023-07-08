@echo off

:: install.bat should be run from the Anaconda command line

:: echo takes arguments that you pass to it through the command line
SET /p db_server="SQL SERVER NAME: "
SET /p db_name="SQL DATABASE NAME: "
SET /p db_user="SQL USERNAME: "
SET /p db_pass="SQL PASSWORD: "
SET /p cites_key="CITES API KEY: "
SET /p iucn_key="IUCN API KEY: "

:: Set up config.ini file
call python config_setup.py %db_server% %db_name% %db_user% %db_pass% %cites_key% %iucn_key%

:: Drop old env
call conda deactivate
call conda env remove --name priority-env

:: Create and activate conda environment
call conda env create priority-env -f environment.yml
call conda activate priority-env

:: Set up required data and files for app
call python database_setup/generate_metadata.py
call python database_setup/taxonomy/generate_tax_rep.py
call python database_setup/get_api_data.py
call python database_setup/generate_dataframes.py
call python database_setup/upload_to_sql.py
call python database_setup/cache_database.py
call python database_setup/cache_scored_data.py