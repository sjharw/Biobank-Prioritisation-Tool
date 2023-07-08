# Required libraries
import json
import aiohttp
import asyncio
import time
import sys
from configparser import ConfigParser

# Get path and API key from config.ini
config = ConfigParser()
config.read("config.ini")
ROOT = config["PATHS"]["root_dir"]

# import bespoke functions
if ROOT not in sys.path:
    sys.path.append(ROOT)

from functions.utils import get_url, get_path_info, validate_json_schema
_, _, _, DB_DIR, _, _ = get_path_info(config)

# import paths and api information
apis = config["API"]
CITES_API_KEY = apis["cites"]
IUCN_API_KEY = apis["iucn"]

# import schemas for validating api response structure
with open(DB_DIR + "schemas/iucn_api.json") as iucn_schema, open(DB_DIR + "schemas/cites_api.json") as cites_schema:
    iucn_schema = json.load(iucn_schema)
    cites_schema = json.load(cites_schema)

#################################################
#------------------ CITES ---------------------##
#################################################
r = get_url(
    url="https://api.speciesplus.net/api/v1/taxon_concepts?",
    headers={"X-Authentication-Token": CITES_API_KEY},
)

# Validate schema
validate_json_schema(r.json(), cites_schema)

# Save json response data to temp folder
with open(ROOT + "/temp/cites_response.json", "w") as file:
    json.dump(r.json(), file)


##################################################
##------------------ IUCN ---------------------##
##################################################
async def get_iucn_page(session, page_number):
    url = f"http://apiv3.iucnredlist.org/api/v3/species/page/{page_number}?token={IUCN_API_KEY}"
    try:
        async with session.get(url) as response:
            if response.text == '{"message":"Token not valid!"}':
                raise Exception("Token not valid!")
            elif response.status == 404:
                print(f"Page {page_number} not found")
            elif response.status != 200:
                raise Exception(
                    f"Request failed with response status: {response.status}"
                )
            else:
                time.sleep(1) # so the server doesnt get overloaded
                return await response.json()
    except aiohttp.ClientError as e:
        print(f"Error occured while getting page {page_number} : {e}")
        return None


async def get_multiple_iucn_pages(page_numbers):
    async with aiohttp.ClientSession() as session:
        tasks = [get_iucn_page(session, page_number) for page_number in page_numbers]
        results = await asyncio.gather(*tasks)
        return results


page_numbers = range(0, 16)  # iucn has a total of 16 pages
json_pages_list = asyncio.run(get_multiple_iucn_pages(page_numbers)) # save list of dictionaries

# Validate schema
validate_json_schema(json_pages_list[1], iucn_schema)

# Save response data to temp folder
with open(ROOT + "/temp/iucn_response.json", "w") as file:
    json.dump(json_pages_list, file)
