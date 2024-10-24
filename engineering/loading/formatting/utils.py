"""
This module contains utility functions for formatting data.
"""

from string import ascii_uppercase

import pandas as pd
import numpy as np
from pydantic import PositiveInt


def get_excel_column_letter(idx: PositiveInt) -> str:
    """
    Convert a column index (1-based) to an Excel column letter.

    :param idx: The column index to convert from an index to Excel column letter
    :type idx: PositiveInt
    :return: The column letter
    :rtype: str
    """
    column_letter: str = ""
    while idx > 0:
        idx, remainder = divmod(idx - 1, 26)
        column_letter = ascii_uppercase[remainder] + column_letter
    return column_letter

def get_cols_widths(dataframe: pd.DataFrame) -> list[int]:
    """
    Get the widths of the columns in the dataframe

    :param dataframe: The dataframe
    :type dataframe: pd.DataFrame
    :return: The widths of the columns
    :rtype: list[int]
    """
    widths = [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]
    # list_width = [max(len(str(val)) for val in dataframe[col].astype(str)) + 2 for col in dataframe.columns]
    return [w + 1 for w in widths]

def trunc_number(number: int, decimals: int) -> float:
    """
    Truncate a number to a specific number of decimals

    :param number: The number to truncate
    :type number: int
    :param decimals: The number of decimals to keep
    :type decimals: int
    :return: The truncated number
    :rtype: float
    """
    factor: int = 10 ** decimals
    truncated_number: float = number.apply(lambda x: np.floor(x * factor) / factor) if isinstance(number, pd.Series) else np.floor(number * factor) / factor
    return truncated_number
