# Biobank-Prioritisation-Tool

The mission of this project is to provide a tool that enables biobanks to enhance the diversity and availability of zoological samples for conservation and research.

## Table of contents
**[About the project](#About-the-project)**<br>
**[Technology](#Technology)**<br>
**[Getting started](#Getting-started)**<br>
**[Project structure](#Project-structure)**<br>
**[Future development](#Future-development)**<br>
**[Acknowledgements](#Acknowledgements)**<br>
**[License](#License)**<br>


## About the project
Biobanks have been established to safeguard existing genetic diversity by freezing biological animal material that can be used in research or later
be defrosted and used to reintroduce genetic diversity into ex-situ and in-situ populations. Unfortunately, biobanks face challenges such as high operational costs and limited funding, and they must prioritise their efforts. This tool has been developed to assist biobanks with prioritising species for sample collection so they can optimise their resource usage and allocation.

This tool takes into account the species **conservation value** (IUCN Category, CITES Appendix, and EDGE Score), 
the **demand** (requests) for samples from that species, 
and the number of **samples** already present within the biobank. 
Species with high conservation value will have higher priority scores because they have greater risk of extinction and greater evolutionary distinctiveness.
The same goes for species with higher demand for samples.
Species with fewer samples in biobanks receive higher scores than those with greater numbers of samples in storage, as a lack of samples pose greater risk of losing that species genetic information.
These category scores are used to calculate a priority score for each species which can be used to rank the species.

The projects adopts an alterated version of the [MAPISCo methodology](https://github.com/DrMattG/MAPISCo) to generate the priority scores.
The method involves converting any string data to a numeric form, normalising the individual dataset scores by diving/ inverting by the maximum, combining the datasets into their corresponding category by taking their mean, applying a weight to this category, and then taking the mean of the weighted categories to produce a priority score that ranks species.

The tool is currently problematic with handling missing data, 
it assigns values of zero to missing data which artificially reduces the overall priority scores, 
thus penalising species that have missing data. 
This issue is due to be addressed in later versions of the tool.

Please note that this application is still in development and may therefore throw up bugs and unexpected errors.

### About the developer
[Sarah](https://www.linkedin.com/in/sarah-j-harwood) is a Data Engineer with a background in genetics and conservation biology. She was introduced into the world of biobanking when she met [Mike Bruford](https://www.cardiff.ac.uk/people/view/81128-bruford-mike) who offered her a placement year with [The Frozen Ark](https://www.frozenark.org/). During this time, Sarah upskilled in Data Engineering in R & SQL. Since her placement year she has worked with various technologies, including Python, PySpark, Neo4j, ArangoDB, and Azure. Using her newfound skills, Sarah has volunteered with CryoArks to re-develop the Prioritisation Tool as a Python Flask application to practice Python Software Development and produce a useful tool that can be used by biobanks. This is her first full-stack application and it is in ongoing development.

### About the datasources

**CryoArks**
<br>
[CryoArks biobank](https://www.cryoarks.org/) is an initiative that aims to bring together the diverse collections of animal frozen material found in museums, zoos, research institutes and universities across the UK to make them accessible to the UK’s research and conservation community. The CryoArks dataset provides counts of the number of samples stored for each species across the CryoArks collection. The dataset provided in this app has been cleaned and processed, it is not the original CryoArks dataset.

**CITES**
<br>
[Convention on International Trade in Endangered Species of Wild Fauna and Flora](https://cites.org/eng/disc/species.php) (CITES) is a multilateral treaty to protect endangered plants and animals from the threats of international trade. CITES operates through a system of permits and certificates that control the import, export, and re-export of protected species. It categorizes species into three appendices based on their conservation status and the level of protection required. Appendix I includes the most endangered species, for which commercial trade is generally prohibited. Appendix II covers species that are not necessarily threatened with extinction but that may become so unless trade is closely controlled. Appendix III lists species protected by at least one member country that requests cooperation from other countries to control their trade. 

CITES provide access to the Species+ database through the [Species+/CITES Checklist API](https://api.speciesplus.net/). Each row of data in the Species+ database represents a single taxon concept (a distinct species) and their corrosponding CITES Appendix. The taxon concept is defined by a unique combination of a scientific name and its corresponding author/year.

**IUCN**
<br>
The [International Union for Conservation of Nature](https://www.iucn.org/) (IUCN) is a globally recognized organization dedicated to promoting sustainable development and the conservation of biodiversity. IUCN maintains the [Red List of Threatened Species](https://www.iucnredlist.org/), a comprehensive database that assesses the conservation status of thousands of species worldwide. The IUCN Red List is a critical indicator of the health of the world’s biodiversity. It provides information about range, population size, habitat and ecology, use and/or trade, threats, and conservation actions that will help inform necessary conservation decisions. IUCN provides access to the Red List database through the [IUCN Red List API](http://apiv3.iucnredlist.org/).

**EDGE**
<br>
[The Evolutionarily Distinct and Globally Endangered](https://www.edgeofexistence.org/species/) (EDGE) organization is a conservation initiative that focuses on identifying and protecting the world's most unique and endangered species. Established by the Zoological Society of London (ZSL), EDGE aims to prioritize species that have few close relatives and are at high risk of extinction. These species often represent distinct branches of the evolutionary tree and have unique adaptations and ecological roles. EDGE provide access to their EDGE lists thought the [EDGE List site](https://www.edgeofexistence.org/edge-lists/).

## What to expect
Once the application has been installed and app.py is running, users can navigate to the website by visiting localhost:5000 in your browser. The website has a landing page called 'home' which provides a brief overview of the project. To see other pages such as 'dataset' and 'upload' page, go to the navigation bar at the top of the page and click on the page links. 

The dataset page displays scores for each category: conservation value, demand, and biobank samples. In addition, the class of each species, percentage of missing data and the priority score derived from the category scores are displayed for each species.

![Alt text](images/display-page.png?raw=true "Dataset page") 

Biobank sample data can be added through the upload page. The added sample data will be displayed alongside the other categories in the dataset page, and it will contribute to the priority score calculated for each species. If no biobanking data has been provided, the user will be redirected to the upload page. When a user uploads their biobank data via the upload page, this data with be displayed and the user will be given an option to add this data to the project. The user is able to download the displayed data in the dataset page using the download button, all downloads can be found in the /downloaded folder inside the project folder.

![Alt text](images/upload-display-page.png?raw=true "Upload display page")

## Technology

### Tech stack
Back-end:
- [Visual Studio Code VSC](https://code.visualstudio.com/) 1.71.2
- [Anaconda3](https://www.python.org/downloads/) 22.11.1
- [Python](https://www.python.org/) 3.9.0
- [Microsoft SQL Server Management Studio](https://learn.microsoft.com/en-us/sql/ssms/release-notes-ssms?view=sql-server-ver16#previous-ssms-releases) 18
- [Microsoft SQL Server](https://www.microsoft.com/en-gb/sql-server/sql-server-downloads) 2019 (x64)
- [SQLAlchemy](https://www.sqlalchemy.org/)

Front-end:
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [getbootstrap](https://getbootstrap.com/docs/5.3/examples/)
- [JQuery](https://jquery.com/)
- [DataTables](https://datatables.net/)
- [Jinja](https://jinja.palletsprojects.com/en/3.1.x/)
- [JavaScript](https://www.javascript.com/)
- [HTML](https://www.w3schools.com/html/)
- [CSS](https://www.w3schools.com/css/)

Linting, formatting and testing:
- [GoogleStyle](https://google.github.io/styleguide/pyguide.html) for formatting
- [Black](https://github.com/psf/black) for linting
- [pytest](https://docs.pytest.org/en/7.2.x/) for testing

### Supported Operating Systems
- [x] Windows
- [ ] Mac
- [ ] Linux


## Getting started 

### Prerequisits
**Setup API accounts**
<br>
This tools relies on API calls to [IUCN red List API](https://apiv3.iucnredlist.org/) and [Species+/CITES Checklist API](https://api.speciesplus.net/). 
You will need setup an account with these organisations and request an API token, you will be prompted to supply these
API tokens when you install the application. Without these tokens, the application will fail to install.

**Download datasets**
<br>
EDGE data is provided in this tool within the <i>/datasets</i> folder. You can replace the 'EDGE_List_2023.xlsx' file with a more recent version of EDGE List data as they become available. Do this by navigating to the [EDGE List site](https://www.edgeofexistence.org/edge-lists/), downloading the most recent EDGE List, unzipping the downloaded folder and placing the file into to the `/datasets` folder in this app. If you replace the EDGE List, the download file will need to be renamed to 'EDGE_List_2023.xlsx' so that the app recognises it, alternatively you can edit the reference to the file in the code.

CryoArk data is also provided within the <i>/datasets</i> folder. You can uplaod the CryoArks data through the upload page to add their biobank data to the tool.

**Setup SQL database (optional)**
<br>
The application provides the user an option to store the datasource data (IUCN, EDGE, and CITES) in an SQL database. If you want to use SQL, you will need to manually setup an SQL database on your device by running the following SQL query `CREATE DATABASE prioritydb`. I'd recommend using [Microsoft SQL Server Management Studio](https://learn.microsoft.com/en-us/sql/ssms/release-notes-ssms?view=sql-server-ver16#previous-ssms-releases) to setup your SQL database.
Note down the name of the database, as well as the server name, and any username or password that is required to login into SQL. You will need this information when you install the app.

Please note that setting up an SQL database is optional and not a requirement for the application to run. Users can opt out of using SQL, this would suit use cases where the app is used in isolation and the user doesn't require frequent access to datasource data (IUCN, CITES, EDGE).

### Download
Download the code by clicking the green 'code' button top right of the README, then clicking 'download zip'. Unzip the downloaded folder and move it to an appropriate location in your device.

### Installation

To setup the application, change to the directory of the app `cd C:/path/to/Prioritization-Tool` and excecute `install.bat` in the Anaconda Prompt, 
this will prompt you for your API details and give you the option to upload the data to an SQL database. If you choose to upload the data to SQL but you dont require a username or password to connect to SQL then pass an empty string `""` as an argument to the Anaconda Prompt when prompted for your SQL details.
The `install.bat` file does the following:
- Sets up a Conda environment called `priority-env` using `environment.yml` that contains all the packages and dependencies required for the app to run
- Generates `config.ini` file by running `config_setup.py` that contains the private Flask, SQL, and API information that you supply via the Conda prompt, as well as paths to folders within the application
- Runs certain files in /database_setup folder to generate the data required for the project

The installation can take some time as Anaconda needs to download all packages and dependencies, make the API calls, and optionally, upload the data into SQL.

If, for any reason, you need to install additional pip packages, navigate to the 
Anaconda prompt, change to the project directory `cd path/to/Prioritization-Tool`, activate the conda enviroment `activate priority-env` and install the named package with `python -m pip install package_name`

### Run
Run the app in the Anaconda prompt with `python app.py`

### Troubleshooting
If you get an Anaconda error after installation, try copying `libcrypto-1_1-x64.*` and `libssl-1_1-x64.*` from *your_anaconda3_path\Library\bin* to *your_anaconda3_path\DLLs* and see if that resolves the issue.

If you get a `DLL load failed while importing _sqlite3` error then you need to download sqlite3 from [here](https://www.sqlite.org/download.html)
and copy and paste the sqlite3 files into your Conda environments DLLs folder.

### Note to developers
This project is still under development and may have some teething issues. 
If you run into a bug, please let me know and I will look into fixing it.
Direct edits or pushes to the main branch in this repository are not permitted. Please contact the [author](https://www.linkedin.com/in/sarah-j-harwood) of the tool if you want to collaborate.


## Project structure

### App folder structure
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

### Testing
 Bespoke functions in the '/functions' folder are tested with the `pytest` module. 
 
 You can run the tests from the Anaconda prompt:
 - Change the path to point at the project directory: `cd path/to/project/folder`
 - Run the tests: `pytest test/*.py`

### Folders and files
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

**Temp**
<br>
API request responses, intermediate tables, and cached data are all saved to the /temp folder. Do not delete this folder, it contains the data required for the app to run.

**Datasets**
<br>
The /datasets folder contains the CryoArks dataset and EDGE 2023 dataset.

**Downloaded**
<br>
The /downloaded folder is where downloads from the application are saved to.

## Future development
This project is in ongoing development. The previous version was developed on the request to have the data in SQL for frequent access and use in other projects. This current version allows user to specify if they want to use an optional SQL database to store the data.

There are some areas I am planning to work on in future editions:
- Replacing fake demand scores with real demand/ request data
- Improving error messaging for more precise error handling
- Handling missing data effectively so it doesn't cause artificially low scores
- Enforcing more rigorous data health checks to avoid unexpected errors/ bugs

## Acknowledgements

[Mike Bruford](https://www.cardiff.ac.uk/people/view/81128-bruford-mike) inspired and directed this project, he provided the methodology implemented here.
Mike was the director of [The Frozen Ark Project](https://www.frozenark.org/) and the lead investigator of [CryoArks](https://www.cryoarks.org/). He sadly passed away in April 2023.

[Mafalda Costa](https://www.cardiff.ac.uk/people/view/80994-bento-costa-mafalda) provided ongoing support for the development of this project. 
Maf is a conservation biologist at Cardiff University and a research associate for CryoArks.

Thank you to [Matthew Grainger](https://github.com/DrMattG) for providing information on the MAPISCo methodology that this project adopts, 
and thank you to [Ian Merrick](https://github.com/sglim2) for supporting the deployment of this tool on CryoArks server.

Thank your to IUCN, CITES, EDGE and CryoArks for your data.

**IUCN**
<br>
<a href="https://www.iucnredlist.org">
IUCN 2022. IUCN Red List of Threatened Species. Version 2022-2
</a> 

**EDGE**
<br>
<a href="https://doi.org/10.1371/journal.pbio.3001991">
The EDGE2 protocol: Advancing the prioritisation of Evolutionarily Distinct and Globally Endangered species 
for practical conservation action Gumbs R, Gray CL, Böhm M, Burfield IJ, Couchman OR, et al. (2023) 
PLOS Biology 21(2): e3001991. 
</a>

**CITES**
<br>
<a href="https://speciesplus.net/">
UNEP (2023). The Species+ Website. Nairobi, Kenya. Compiled by UNEP-WCMC, Cambridge, UK.
</a>

**CryoArks**
<br>
<a href="https://www.cryoarks.org/database/">
CryoArks (2019). CryoArks Database.
</a>

**MAPISCo**
<br>
<a href="(http://www.cbsg.org/sites/cbsg.org/files/Prioritizing%20Species%20for%20Conservation%20Planning.pdf">
Method for the Assesment of Priorities for International Species Conservation (MAPISCo, Defra)
</a>

## Credits
This tool was built soley by [Sarah Harwood](https://www.linkedin.com/in/sarah-j-harwood) [@sjharw](https://github.com/sjharw)

## License
This app is published under a General Public License (GPL) v2.0. Please reference the original author of this tool [@sjharw](https://github.com/sjharw) in any derivative/ modified/ copied versions of this work.

The goal of the GPL v2.0 is to promote the free sharing and collaboration of software. It ensures that everyone has the freedom to use, modify, and share software while respecting the rights of others. 

The GPL grants you the following freedoms:
- You can use the software without paying or needing permission
- You can modify the software to suit you needs, but you must share your modifications under GPL v2.0
- You can share the software, but you must include the GPL v2.0 license along with any distributions
- You cannot prevent others from using, modifying, or sharing the software as the license permits

