import pandas as pd

from typing import Any


def sellin_format(
    worksheet: Any,
    sheet_name: str,
    dataframe: pd.DataFrame,
    data_additional: dict[str, pd.DataFrame],
    options: dict[str, Any]
) -> None:
    """
    Load dataframes into an Excel file and apply formatting.

    :param worksheet: The worksheet to apply formatting to
    :type worksheet: Any
    :param sheet_name: The name of the sheet
    :type sheet_name: str
    :param dataframe: The exported dataframe
    :type dataframe: pd.DataFrame
    :param data_additional: Additional data to be saved
    :type data_additional: dict[str, pd.DataFrame]
    :param options: The selected options
    :type options: dict[str, Any]
    """