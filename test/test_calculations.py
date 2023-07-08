import pytest
import pandas as pd
import numpy as np
from functions.calculations import Calculations, priority_score, enforce_float


@pytest.fixture
def expected_series():
    expected_series = pd.Series(
        data={"a": 1, "b": 2, "c": 0, "d": 0}, index=["a", "b", "c", "d"]
    )
    return expected_series


def test_enforce_int():
    """
    enforce_int() converts none and str type to int
    """
    assert np.issubdtype(
        enforce_float(pd.Series([200, "58", None, float("nan")])), float
    )  # handles both None and NaN
    with pytest.raises(
        ValueError,
        match=r"Error converting column to float type.",
    ):
        enforce_float(pd.Series(["this is not a number", "this should raise an error"]))


def test_divide_max(expected_series):
    """
    Each row is divided by
    highest number in column.
    """
    calc = Calculations(expected_series)
    assert list(calc.divide_max()) == [
        0.5,
        1.0,
        0.0,
        0.0,
    ]  # 1 is divided by 2, 2 is divided by 2, etc.


def test_invert_max(expected_series):
    """
    Each row is divided by
    highest number in column
    and taken away from 1.
    """
    calc = Calculations(expected_series)
    assert list(calc.invert_max()) == [
        0.5,
        0.0,
        1.0,
        1.0,
    ]  # 1 is divided by 2 and taken away from 1, 2 is divided by 2 and taken away from 1, etc.


def test_priority_score():
    """
    Each row is divided by
    highest number in column
    and taken away from 1.
    If strings are given, they
    get appended together and
    divided by number of columns.
    """
    test_df = pd.DataFrame(
        {
            "full_name": ["sarah", "john", "bob", "kitty", "barny"],
            "height": [5, 6, 5, 4, 7],
            "weight": [57, 76, 58, 49, 83],
        }
    )
    # assert average of rows are taken and sorted by desc
    assert list(priority_score(test_df)["priority_score"]) == [
        45.0,
        41.0,
        31.5,
        31.0,
        26.5,
    ]
