import pytest
import jsonschema
import numpy as np
import pandas as pd
from functions.utils import multi_dict_replace_rows, filter_species, rename_taxonomy, nested_dicts_to_df, generate_demand, validate_json_schema, validate_df_schema, columns_to_snake_case, clean_dataframe

@pytest.fixture
def test_dataframe():
    return pd.DataFrame({
        'taxonid': [3, 4],
        'kingdom': ['Animalia', 'Animalia'],
        'phylum': ['Mollusca', 'Mollusca'],
        'class': ['Gastropoda', 'Gastropoda'],
        'order': ['Stylommatophora', 'Stylommatophora'],
        'family': ['Endodontidae', 'Endodontidae'],
        'genus': ['Aaadonta', 'Aaadonta'],
        'full_name': ['Aaadonta angaurana', 'Aaadonta constricta'],
        'taxonomic_authority': ['Solem, 1976', '(Semper, 1874)'],
        'infra_rank': [None, None],
        'infra_name': [None, None],
        'population': [None, None],
        'iucn_category': ['CR', 'EN'],
        'main_common_name': [None, None]
    })

def test_multi_dict_replace_rows():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": ["hi", "hello", None]})
    rep_dicts = {"A": {1: 10}, "B": {4: 40}, "C": {"hello": "goodbye"}}
    expected_df = pd.DataFrame(
        {"A": [10, 2, 3], "B": [40, 5, 6], "C": ["hi", "goodbye", None]}
    )
    result_df = multi_dict_replace_rows(df, rep_dicts)
    assert result_df.equals(expected_df), f"Expected {expected_df}, but got {result_df}"


def test_rename_taxonomy():
    """
    Rename_col function renames all taxa columns
    to a standardised format, while
    leaving non-taxa columns untouched.
    """
    df = pd.DataFrame(
        {
            "kingdom_x": ["animalia"],
            "phylum_x": ["chordata"],
            "class_x": ["Mammalia"],
        }
    )
    result_df = rename_taxonomy(df)
    expected_df = pd.DataFrame(
        {
            "kingdom": ["Animalia"],
            "phylum": ["Chordata"],
            "class": ["Mammalia"],
        }
    )
    assert result_df.equals(expected_df), f"Expected {expected_df}, but got {result_df}"

def test_filter_species():
    test_df = pd.DataFrame({
        'taxonid': [3, 4, 3, 2, 5, 6],
        'full_name': ['Aaadonta angaurana', None, 'Aaadonta angaurana', 'Acanthixalus sonjae', 'Sphenodon punctatus guntheri', np.nan],
    }, index= [0, 1, 2, 3, 4, 5])
    expected_df = pd.DataFrame({
        'taxonid': [3, 2],
        'full_name': ['Aaadonta angaurana', 'Acanthixalus sonjae'],
    }, index= [0, 1])
    result_df = filter_species(test_df)
    assert result_df.equals(expected_df)

def test_filter_species_fail():
    test_df = pd.DataFrame({
        'taxonid': [3, 4, 3, 2, 5, 6],
        'species': ['Aaadonta angaurana', None, 'Aaadonta angaurana', 'Acanthixalus sonjae', 'Sphenodon punctatus guntheri', np.nan],
    }, index= [0, 1, 2, 3, 4, 5])
    with pytest.raises(ValueError) as error:
        filter_species(test_df)
    # Assert the specific error message
    assert str(error.value) == "Column 'full_name' is not present in dataset, cleaning failed."


def test_nested_dicts_to_df():
    """
    Function converts nested dicts to df using key, and raises a KeyError if
    a key is supplied that isn't in the nested dictionary.
    """
    nested_dicts = [
        {
            "person": [
                {"first_name": "John", "last_name": "Doe"},
                {"first_name": "Jane", "last_name": "Doe"},
            ]
        },
        {
            "person": [
                {"first_name": "Bob", "last_name": "Smith"},
                {"first_name": "Alice", "last_name": "Johnson"},
            ]
        },
    ]
    expected_df = pd.DataFrame(
        [
            {"first_name": "John", "last_name": "Doe"},
            {"first_name": "Jane", "last_name": "Doe"},
            {"first_name": "Bob", "last_name": "Smith"},
            {"first_name": "Alice", "last_name": "Johnson"},
        ]
    )
    result_df = nested_dicts_to_df(nested_dicts, "person")
    pd.testing.assert_frame_equal(expected_df, result_df)
    with pytest.raises(
        KeyError, match=r"The key 'error' was not found in the nested dictionaries."
    ):
        nested_dicts_to_df(nested_dicts, "error")

def test_generate_demand():
    """
    Tests if the generate_demand() function can handle duplicate
    values and indexes without throwing an error.
    """
    test_df = pd.DataFrame(data = {'full_name': ['Banana', 'Banana', 'Apple', 'Pear', 'Peppers', 'Carrots'], 'class': ['Fruit', 'Fruit',  'Fruit', 'Fruit', 'Vegetable', 'Vegetable']}, index = ['1', '1', '2', '2', '4', '5'])
    test_scores = {'Vegetable': 10, 'Fruit': 3, 'Dairy': 6}
    result_df = generate_demand(test_df, test_scores)
    assert all([round(r) in range(0,7) for r in (result_df[result_df['class'] == 'Fruit']["demand"])])
    assert all([round(r) in range(7,14) for r in (result_df[result_df['class'] == 'Vegetable']["demand"])])

def test_validate_json_schema():
    # Create a valid JSON data and schema
    json_data = {"name": "John", "age": 30}
    schema = {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}}

    # The function should not raise any errors
    validate_json_schema(json_data, schema)

def test_invalid_json_schema():
    # Create an invalid JSON data and schema
    json_data = {"name": "John", "age": "30"}  # 'age' should be an integer, but it's a string
    schema = {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}}

    # The function should raise a ValueError with a specific message
    with pytest.raises(jsonschema.exceptions.ValidationError) as error:
        validate_json_schema(json_data, schema)

def test_validate_df_schema_pass(test_dataframe):
    # Define the schema
    schema = {
        'taxonid': int,
        'kingdom': object,
        'phylum': object,
        'class': object,
        'order': object,
        'family': object,
        'genus': object,
        'full_name': object,
        'taxonomic_authority': object,
        'infra_rank': object,
        'infra_name': object,
        'population': object,
        'iucn_category': object,
        'main_common_name': object
    }

    # Validate the DataFrame against the schema
    validate_df_schema(test_dataframe, schema)

    assert True


def test_validate_df_schema_fail_ValueError(test_dataframe):
    # Define the schema
    schema = {
        'taxonid': str,
        'kingdom': str,
        'phylum': str,
        'class': str,
        'order': str,
        'family': str,
        'genus': str,
        'full_name': str,
        'taxonomic_authority': str,
        'infra_rank': str,
        'infra_name': str,
        'population': str,
        'iucn_category': str,
        'main_common_name': str
    }

    with pytest.raises(ValueError) as error:
        validate_df_schema(test_dataframe, schema)

def test_validate_df_schema_fail_KeyError(test_dataframe):
    # Define the schema
    schema = {
        'another_column': int,
        'kingdom': str,
        'phylum': str,
        'class': str,
        'order': str,
        'family': str,
        'genus': str,
        'full_name': str,
    }

    with pytest.raises(KeyError) as error:
        validate_df_schema(test_dataframe, schema)

    # Assert the specific error message
    assert str(error.value) == str(KeyError("Expected columns are missing from dataframe: ['another_column']"))

def test_columns_to_snake_case():
    test_df = pd.DataFrame(
        [
            {"first naME": "John", "last Name": "Doe", "HairColour": "black"},
        ]
    )
    expected_df = pd.DataFrame(
        [
            {"first_name": "John", "last_name": "Doe", "haircolour": "black"},
        ]
    )
    result_df = columns_to_snake_case(test_df)
    pd.testing.assert_frame_equal(expected_df, result_df)

def test_clean_dataframe():
    """
    Larger test to check if the multiple functions in the 
    clean_dataset() function are giving overall expected output
    """
    taxa_dict = {'class': {}, 'order':{}, 'family': {}}
    test_df= pd.DataFrame({
        'taxonid': [0, 1, 2, 3, 4, 2],
        'kingdom_name': ['Animalia', None, 'Animalia', 'Animalia', None, 'Animalia'],
        # 'phylum': ['Mollusca', None, 'Mollusca', 'Chordata', None, 'Mollusca'],
        'class name': ['Gastropoda', None, 'Gastropoda', 'Reptilia', None, 'Gastropoda'],
        'order': ['Stylommatophora', None, 'Stylommatophora', 'Rhynchocephalia', None, 'Stylommatophora'],
        'Family Name': ['Endodontidae', None, 'Endodontidae', 'Sphenodontidae', None, 'Endodontidae'],
        'genus': ['Aaadonta', None, 'Aaadonta', 'Sphenodon', None, 'Aaadonta'],
        'full_name': ['Aaadonta angaurana', None, 'Aaadonta constricta', 'Sphenodon punctatus guntheri', np.nan, 'Aaadonta constricta'],
    })
    expected_df= pd.DataFrame({
        'taxonid': [0, 2],
        'kingdom': ['Animalia', 'Animalia'],
        # 'phylum': ['Mollusca','Mollusca'],
        'class': ['Gastropoda', 'Gastropoda'],
        'order': ['Stylommatophora', 'Stylommatophora'],
        'family': ['Endodontidae', 'Endodontidae'],
        'genus': ['Aaadonta', 'Aaadonta'],
        'full_name': ['Aaadonta angaurana', 'Aaadonta constricta'],
    })
    result_df = clean_dataframe(test_df, taxa_dict)
    assert result_df.equals(expected_df)