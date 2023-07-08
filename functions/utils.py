import re
import numpy as np
import pandas as pd
import requests
import json
import jsonschema
import warnings
from itertools import chain
from flask import jsonify

def get_db_info(config):
    """
    Extracts database information from a configuration dictionary and returns it as a tuple.
    Unpack the tuple with the following code: 
    `SERVER, USERNAME, PASSWORD, DRIVER, DB_NAME = get_db_info(config)`.
    If you need to only unpack some variable, use underscores (_) to ignore unneeded variables when unpacking a tuple.

    Parameters:
        config (dict): A dictionary containing configuration information, including database connection details.

    Returns:
        (tuple): A tuple containing the server name, username, password, driver, and database name in that order.
    """
    dbinfo = config["DATABASE"]
    server = dbinfo["server_name"]
    username = dbinfo["username"]
    password = dbinfo["password"]
    driver = dbinfo["driver"]
    db_name = dbinfo["database_name"]
    return server, username, password, driver, db_name

def get_path_info(config):
    """
    Extracts path information from a configuration dictionary and returns it as a tuple.
    Unpack the tuple with the following code: 
    `ROOT_DIR, TEMP_DIR, TAXON_DIR, DB_DIR, DS_DIR, DOWNLOAD_DIR = get_path_info(config)`.
    If you need to only unpack some variable, use underscores (_) to ignore unneeded variables when unpacking a tuple.

    Parameters:
        config (dict): A dictionary containing configuration information, including file paths.

    Returns:
        (tuple): A tuple containing the root directory, temporary directory, taxa directory, database directory, dataset directory, and downloads directory in that order.
    """
    paths = config["PATHS"]
    root_dir = paths["root_dir"]
    temp_dir = paths["temp_dir"]
    taxon_dir = paths["taxa_dir"]
    db_dir = paths["db_dir"]
    dataset_dir = paths["dataset_dir"]
    download_dir = paths["download_dir"]
    return root_dir, temp_dir, taxon_dir, db_dir, dataset_dir, download_dir


def multi_dict_replace_rows(df: pd.DataFrame, rep_dicts: dict):
    """
    Replaces values (rows) in multiple columns
    with the corrosponding values in each dictionary.

    Parameters:
        df (pandas.dataframe): dataframe
        rep_dict (dict): dictionary containing dictionaries

    Returns:
        df (pandas.dataframe): dataframe
    """
    # for each dictionary
    for key in rep_dicts:
        # replace values using dictionary
        df = df.replace(rep_dicts[key])
    return df


def rename_taxonomy(df: pd.DataFrame):
    """
    This function renames the columns of the dataframe
    to match the taxonomy related terms "kingdom",
    "phylum", "class", "order", "family", "genus".
    It capitalizes the contents of the columns after
    renaming them.

    Parameters:
        df (pandas.DataFrame): dataframe to be renamed

    Returns:
        pandas.DataFrame: dataframe with renamed and capitalized columns

    Example:
        df = pd.DataFrame({"kingdom_name": ["Animalia"], "taxa_phylum": ["Chordata"], "class_x": ["Mammalia"]})
        renamed_df = rename_taxonomy(df)
        print(renamed_df)
        >>>   kingdom  phylum   class
                Animalia  Chordata  Mammalia
    """
    # column names that will relace df column names
    rep_col = ["kingdom", "phylum", "class", "order", "family", "genus"]
    # create dictionary of matched column and replacement columns
    rep_dict = {
        col: rep
        for col in list(df.columns)
        for rep in rep_col
        if re.findall(rep, col, re.IGNORECASE) != []
    }
    # rename df columns using rep_dict
    df = df.rename(columns=rep_dict)
    # capatilise the rows of every column
    for column in df.columns:
        if column in rep_col:
            # capitalize the column values and assign them back to the dataframe
            df[column] = df[column].str.capitalize()
    return df

def filter_species(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter species names, drop null values, and remove duplicate entries for the 'full_name' column.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the species data.

    Returns:
        pandas.DataFrame: The filtered DataFrame with unique species names and without any null values or duplicate entries.

    Raises:
        ValueError: if 'full_name' column isnt present in dataframe
        
    """
    if "full_name" not in df.columns:
        raise ValueError("Column 'full_name' is not present in dataset, cleaning failed.")
    # Drop rows where full_name is null
    df = df[df['full_name'].notna()]
    # Filter to only include species (not genus or subspecies)
    df = df[df['full_name'].str.match("[A-Z]{1}[a-z]+\s[a-z]+$")]
    # Drop duplicates to ensure full_name is unique
    df = df.drop_duplicates(subset='full_name', keep='first')
    # Reset index as some rows may have dropped
    df = df.reset_index(drop=True)
    return df

def nested_dicts_to_df(nested_dicts: dict, key: str):
    """
    Converts a list of nested dictionaries into a pandas DataFrame.

    Parameters:
        nested_dicts (list): A list of dictionaries, where each dictionary contains another dictionary
        key (str): The key of the nested dictionary to extract and convert into the DataFrame

    Returns:
        pandas.DataFrame: A DataFrame containing the extracted and flattened data from the nested dictionaries

    Example:
        nested_dicts = [{"person": [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]},
                        {"person": [{"name": "Jim", "age": 40}, {"name": "Joan", "age": 35}]}]
        df = nested_dicts_to_df(nested_dicts, "person")
        print(df)
        >>>   name  age
                John   30
                Jane   25
                Jim    40
                Joan   35
    """
    try:
        # Extract nested dicts that match dict key
        nested_dicts = [d[key] for d in nested_dicts]
        # Convert multi dimensional (nested) python list into a single list
        nested_dicts = list(chain.from_iterable(nested_dicts))
        # Convert list of dicts to single dataframe
        df = pd.DataFrame.from_dict(nested_dicts)
    except KeyError:
        raise KeyError(f"The key '{key}' was not found in the nested dictionaries.")
    return df

def get_url(url: str, headers: str = "") -> requests.Response:
    """ 
    Makes get request using requests library to 
    given url.

    Args:
        url
        headers

    Returns:
        response: request response object

    Raises:
        requests.exceptions.HTTPError ("Token not valid!"): Provided token is not accepted
        requests.exceptions.HTTPError (HTTPError. Request failed with response status: {response.status_code}, see the following link for more detail on this status: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{response.status_code})
        requests.exceptions.ConnectionError (Connection Error. Error connecting to server url:{url}. Following error raised: {e})
        requests.exceptions.RequestException (Request Exception. An error occurred while making the request: {e})
    """
    try:
        response = requests.get(url=url, headers=headers)
    except requests.exceptions.ConnectionError as e:
        raise requests.exceptions.ConnectionError(f"Connection Error. Error connecting to server url:{url}. Following error raised: {e}")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"An error occurred while making the request: {e}")
    if response.text == '{"message":"Token not valid!"}':
        raise requests.exceptions.HTTPError("Token not valid!")
    elif response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError. Request failed with response status: {response.status_code}, see the following link for more detail on this status: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{response.status_code}")
    else:
        pass
    return response


def generate_demand(taxonomy_df: pd.DataFrame, demand_scores: json) -> pd.DataFrame:
    """
    Generates demand scores for species based on their class.
    The scores follow a random normal distribution around a
    specified mean for each class.

    Parameters:
    taxonomy_df (pandas.DataFrame):
        Daraframe that contains a column named 'class' that
        corresponds to the class of the species, and a column
        named 'full_name' that corresponds to the full scientific
        name of the species.
    demand_scores (json):
        A dictionary of unique species class names (keys) and
        their integers (values). The integers represents the mean
        number of requests for biological samples from that class.

    Returns:
    demand_df (pandas.DataFrame):
        DataFrame that contains the demand scores for each species.
        The DataFrame has columns 'demand' (the demand score),
        'full_name' (the full scientific name of the species),
        and 'class' (the class of the species).

    Example:
    >>> taxonomy_df = pd.DataFrame({'full_name': ['Species 1', 'Species 2', 'Species 3'], 'class': ['Class A', 'Class B', 'Class B']})
    >>> demand_df = generate_demand(taxonomy_df, demand_scores)
    >>> demand_df
               full_name     class  demand
    0        Species 1   Class A       2
    1        Species 2   Class B       6
    2        Species 3   Class B       7
    """
    # group full_name by class
    grouped = (
        taxonomy_df.groupby("class")["full_name"]
        .apply(list)
        .reset_index(name="full_name")
    )
    # count number of species in each class
    grouped["no_species"] = [len(species) for species in grouped["full_name"]]
    # add class demand scores to data
    grouped["demand_scores"] = grouped["class"].map(demand_scores)
    # generate demand scores for each species based on class scores
    demand_data = []
    for _, row in grouped[["demand_scores", "no_species"]].iterrows():
        demand_data.append(
            np.ceil(
                np.random.normal(
                    loc=row["demand_scores"], scale=1, size=int(row["no_species"])
                )
            )
        )
    # create df of results
    demand_df = pd.DataFrame(
        {
            "demand": demand_data,
            "full_name": grouped["full_name"],
            "class": grouped["class"],
        }
    )
    demand_df = demand_df.apply(pd.Series.explode).reset_index(drop=True)
    return demand_df

def get_json_response(json_data: json, data: pd.DataFrame):
    """
    Gets JSON data from DataTables AJAX request, filters, sorts, and paginates the data, 
    and constructs a JSON response in the format expected by DataTables.
    """

    # Get the updated draw, start, length, and search parameters
    draw = int(json_data.get('draw'))
    start = int(json_data.get('start'))
    length = int(json_data.get('length'))
    search = str(json_data.get("search"))
    order = (json_data.get("order"))
    columns = (json_data.get("columns"))

    try:
        classSelected = (json_data.get("classSelected"))
        if classSelected:
            data = data[data["class"] == classSelected]
    except:
        pass

    # Search for term in df if one is given
    if search:
        search_result = data['full_name'].str.contains(search, case=False)
        data = data[search_result]

    # Order by column asc/ desc
    indx_cols = list(enumerate([c['data'] for c in columns]))
    order_col = [c for i, c in indx_cols if i == order[0]['column']]
    order_dir = order[0]['dir']
    if order_dir == 'asc':
        data = data.sort_values(order_col, ascending=True)
    if order_dir == 'desc':
        data = data.sort_values(order_col, ascending=False)

    # Get the total number of data records (rows)
    total_records = len(data)

    # Get the data for the current selected page
    data = data.iloc[start:start + length]

    # Construct the JSON response in the format expected by DataTables
    data_dict = data.to_dict('records')

    response = {
        'draw': draw,
        'start': start,
        'length': length,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data_dict
    }

    return jsonify(response)

def nonnumeric_rows(df: pd.DataFrame, colm: str) -> list:
    """
    Takes a dataframe and column name and 
    returns a list of rows that
    cannot be coerced into numeric type.

    Parameters:
    df (pandas.DataFrame):
        Dataframe containing numeric data
    colm (str):
        Column expected to contain numeric data

    Returns:
    nonnumeric_list (list):
        List of rows that cant be converted to numeric type
    """
    numeric_conversion_series = pd.to_numeric(df[colm], errors='coerce')
    nonnumeric_series = numeric_conversion_series.isna()
    nonnumeric_list = df[nonnumeric_series][colm].to_list()
    return nonnumeric_list

def missing_data_rows(df: pd.DataFrame) -> list:
    """ 
    Takes a df and checks every column 
    for missing data then returns the indexes
    at which data is missing, taking into
    account column names as the first row.

    Args: 
        df (pd.DataFrame): dataframe containing missing data

    Returns:
        missing_list (list): list of indexes at which data is missing

    """
    missing_rows = df.index[df.isnull().any(axis=1)]
    missing_list = list(df.loc[missing_rows].index + 2) # add 1 as first row will be column names
    return missing_list

def duplicate_rows(df: pd.DataFrame, colm: str) -> list:
    """ 
    Finds duplicate enteries in a column
    and returns these enteries.

    Args: 
        df (pd.DataFrame): dataframe containing duplicate data
        colm (str): column wiht duplicates in

    Returns:
        dup_rows_list (list): list of duplicated values
    """
    dup_rows_list = list(df[df.duplicated([colm], keep=False)][colm].drop_duplicates())
    return dup_rows_list

def validate_json_schema(json_data: dict, schema: dict) -> None:
    """
    Validates the given JSON data against the given JSON schema.

    Args:
        json_data (dict): A dictionary containing the JSON data to be validated.
        schema (dict): A dictionary containing the JSON schema to validate against.

    Returns:
        None

    Raises:
        ValueError: If the JSON data does not conform to the schema.

    """
    try:
        jsonschema.validate(json_data, schema)
        print("JSON data conforms to the schema")
    except jsonschema.SchemaError as e:
        raise jsonschema.exceptions.ValidationError("Failed to validate response JSON. Response data does not conform to the schema:")
    
def validate_df_schema(df: pd.DataFrame, schema: dict) -> None:
    """
    Validate the DataFrame against a given schema.

    Checks if the DataFrame columns match the expected schema columns and if their types match the expected types.
    Raises a KeyError if unexpected columns are present or if expected columns are missing.
    Raises a ValueError if a column does not match the expected type.

    Args:
        df (pd.DataFrame): The DataFrame to validate.
        schema (dict): The schema representing the expected columns as keys and their expected types as values.

    Raises:
        warnings.warn: If unexpected columns are present
        KeyError: If expected columns are missing in the DataFrame.
        ValueError: If a column's type does not match the expected type.
    """
    # Check for missing columns
    unexpected_cols = sorted(list(set(df.columns)-set(schema.keys())))
    missing_cols = sorted(list(set(schema.keys())-(set(df.columns))))

    if unexpected_cols:
        warnings.warn(f"Unexpected columns present in dataframe: {list(unexpected_cols)}")
    if missing_cols:
         raise KeyError(f"Expected columns are missing from dataframe: {list(missing_cols)}")

    # Check columns match expected types
    for col, expected_type in schema.items():
        is_expected_type = all(isinstance(value, expected_type) or value is None or value is np.nan for value in df[col])
        if not is_expected_type:
            raise ValueError(f"Error: Column '{col}' does not match the expected schema of '{expected_type.__name__}'.")

def str_to_snake_case(column_name: str) -> str:
    """
    Converts a string to snake case.

    Args:
        column_name (str): The string to convert.

    Returns:
        str: The string converted to snake case.
    """
    snake_string = column_name.replace(' ', '_').lower()
    return snake_string


def columns_to_snake_case(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the column names of a DataFrame to snake case.

    Args:
        df (pd.DataFrame): The DataFrame whose column names need to be converted.

    Returns:
        pd.DataFrame: The DataFrame with column names converted to snake case.
    """
    df.columns = [str_to_snake_case(col) for col in df.columns]
    return df

def clean_dataframe(df: pd.DataFrame, taxa_dict: dict) -> pd.DataFrame:
    """
    Cleans the given DataFrame by standardizing column names, 
    filtering out nulls, duplicate and non-species rows, 
    and replacing incorrect taxonomy with up-to-date taxonomic values.
    DataFrame must include 'full_name' column otherwise error raised.
    
    Args:
        df (pandas.DataFrame): DataFrame to be cleaned
        
    Returns:
        df (pandas.DataFrame) cleaned DataFrame
    """
    # Standardise column names
    df = rename_taxonomy(df)
    df = columns_to_snake_case(df)
    # Filter species
    df = filter_species(df)
    # Replace incorrect taxonomy
    df = multi_dict_replace_rows(df, taxa_dict)
    return df