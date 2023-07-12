@echo off

:: install.bat should be run from the Anaconda command line

echo Setting up Conda environment...

:: Drop old env
call conda deactivate
call conda env remove --name priority-env

:: Create and activate conda environment
call conda env create --quiet priority-env -f environment.yml
call conda activate priority-env

echo Conda environment setup successfully

echo Do you want to upload data to SQL? (y/n)
set /p upload=

:: echo takes arguments that you pass to it through the command line
SET /p cites_key="CITES API KEY: "
SET /p iucn_key="IUCN API KEY: "

if /i "%upload%"=="y" (
    :: echo takes arguments that you pass to it through the command line
    SET /p db_server="SQL SERVER NAME: "
    SET /p db_name="SQL DATABASE NAME: "
    SET /p db_user="SQL USERNAME: "
    SET /p db_pass="SQL PASSWORD: "
    :: Set up config.ini file
    call python config_setup.py %db_server% %db_name% %db_user% %db_pass% %cites_key% %iucn_key%
    REM Run all files here when the user selects 'y'
    echo Setting up app data and uploading to SQL
    :: Set up required data and files for app
    call python database_setup/generate_metadata.py
    call python database_setup/taxonomy/generate_tax_rep.py
    call python database_setup/get_api_data.py
    call python database_setup/generate_dataframes.py
    call python database_setup/upload_to_sql.py
    call python database_setup/cache_sql_database.py
    call python database_setup/generate_scored_dataset.py
) else (
    echo Skipping data upload to SQL.
    :: Set up config.ini file
    call python config_setup.py "" "" "" "" %cites_key% %iucn_key%
    REM Run only specific files here when the user selects 'n'
    echo Setting up app data
    :: Set up required data and files for app
    call python database_setup/generate_metadata.py
    call python database_setup/taxonomy/generate_tax_rep.py
    call python database_setup/get_api_data.py
    call python database_setup/generate_dataframes.py
    call python database_setup/generate_database.py
    call python database_setup/generate_scored_dataset.py
)

echo Application has finished installing