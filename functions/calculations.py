import pandas as pd


def enforce_float(pd_series: pd.Series):
    """
    Convert numbers from str or None to float type. None values are assigned 0.

    Parameters:
        pd_series (pd.Series): pandas series

        pd_series (pd.Series): pandas series with float type
    """
    # NaNs are converted to 0 and enforced to float type
    try:
        pd_series = pd_series.fillna(0).astype(float)
    except ValueError:
        raise ValueError(
            "Error converting column to float type."
        )
    return pd_series


class Calculations:
    """
    Calculations class.
    Performs calculations on pandas series of int type.
    """

    usecase = "Performing calculations on data"

    def __init__(self, series):
        self.series = enforce_float(series)
        self.max_value = self.series.max()

    def divide_max(self):
        """
        Divides each row by the maximum row value of the column.
        Datatype of column must be integer.
        """

        self.series = self.series.apply(lambda row: row / self.max_value)
        return self.series

    def invert_max(self):
        """
        Divides each row by the maximum row value of the column
        and takes this value away from 1.
        Datatype of column must be integer.
        """
        self.series = self.series.apply(lambda row: 1 - (row / self.max_value))
        return self.series

def priority_score(df: pd.DataFrame):
    """
    Calculates the average score across int columns.
    Appends this score to a new column called 'priority_score'.

    Parameters:
        df (pd.DataFrame)

    Returns:
        df (pd.DataFrame): dataframe with a 'priority_score' column
    """
    int_cols = [
        col
        for col in df.columns
        if col
        not in [
            "full_name",
            "class",
            "phylum",
            "kingdom",
            "genus",
            "species",
            "subspecies",
            "null_percent"
        ]
    ]
    df[int_cols] = df[int_cols].apply(enforce_float)
    df["priority_score"] = (df[int_cols].sum(axis="columns")) / len(int_cols)
    # Calculate priority scores based on columns containing data only
    # df["not_nulls"] = df[int_cols].notnull().count(axis=1)
    # df["priority_score"] = (df[int_cols].sum(axis="columns")) / df["not_nulls"]
    df = df.sort_values("priority_score", ascending=False)  # sort by priority score
    return df

