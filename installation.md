# Installation Guide

## Prerequisits
### Setup API accounts
This tools relies on API calls to [IUCN red List API](https://apiv3.iucnredlist.org/) and [Species+/CITES Checklist API](https://api.speciesplus.net/). 
You will need setup an account with these organisations and request an API token, you will be prompted to supply these
API tokens when you install the application. Without these tokens, the application will fail to install.

### Download datasets
EDGE data is provided in this tool within the <i>/datasets</i> folder. You can replace the 'EDGE_List_2023.xlsx' file with a more recent version of EDGE List data as they become available. Do this by navigating to the [EDGE List site](https://www.edgeofexistence.org/edge-lists/), downloading the most recent EDGE List, unzipping the downloaded folder and placing the file into to the `/datasets` folder in this app. If you replace the EDGE List, the download file will need to be renamed to 'EDGE_List_2023.xlsx' so that the app recognises it, alternatively you can edit the reference to the file in the code.

CryoArk data is also provided within the <i>/datasets</i> folder. You can upload the CryoArks data through the upload page to add their biobank data to the tool.

### Setup SQL database (optional)
The application provides the user an option to store the datasource data (IUCN, EDGE, and CITES) in an SQL database. If you want to use SQL, you will need to manually setup an SQL database on your device by running the following SQL query `CREATE DATABASE prioritydb`. I'd recommend using [Microsoft SQL Server Management Studio](https://learn.microsoft.com/en-us/sql/ssms/release-notes-ssms?view=sql-server-ver16#previous-ssms-releases) to setup your SQL database.
Note down the name of the database, as well as the server name, and any username or password that is required to login into SQL. You will need this information when you install the app.

Please note that setting up an SQL database is optional and not a requirement for the application to run. Users can opt out of using SQL, this would suit use cases where the app is used in isolation and the user doesn't require frequent access to datasource data (IUCN, CITES, EDGE).

## Install app
Download the code by clicking the green 'code' button top right of the README, then clicking 'download zip'. Unzip the downloaded folder and move it to an appropriate location in your device.

To setup the application, change to the directory of the app `cd C:/path/to/Biobank-Prioritisation-Tool` and excecute `install.bat` (for Windows) or `install.sh` (for Linux) in the Anaconda Prompt, this will prompt you for your (CITES and IUCN) API details and give you the option to upload the data to an SQL database. If you choose to upload the data to SQL but you dont require a username or password to connect to SQL then pass an empty string `""` as an argument to the Anaconda Prompt when prompted for your SQL details.

The `install.bat` file does the following:
- Sets up a Conda environment called `priority-env` using `requirements.txt` that contains all the packages and dependencies required for the app to run
- Generates `config.ini` file by running `config_setup.py` that contains the private Flask, SQL, and API information that you supply via the Conda prompt, as well as paths to folders within the application
- Runs certain files in /database_setup folder to generate the data required for the project

The installation can take some time as Anaconda needs to download all packages and dependencies, make the API calls, and optionally, upload the data into SQL.

If, for any reason, you need to install additional pip packages, navigate to the 
Anaconda prompt, activate the conda enviroment `activate priority-env` and install the named package with `python -m pip install <package_name>`.


## Troubleshooting
If you get an Anaconda error after installation, try copying `libcrypto-1_1-x64.*` and `libssl-1_1-x64.*` from *your_anaconda3_path\Library\bin* to *your_anaconda3_path\DLLs* and see if that resolves the issue.

If you get a `DLL load failed while importing _sqlite3` error then you need to download sqlite3 from [here](https://www.sqlite.org/download.html)
and copy and paste the sqlite3 files into your Conda environments DLLs folder.