"""
A module for formatting in the engineering.loading.formatting package.
"""

import logging

import pandas as pd
from typing import Any

from engineering.loading.sellin.sellin_format import sellin_format
from engineering.loading.sellout.sellout_format import sellout_format

logger: logging.Logger = logging.getLogger(__name__)


def format_worksheet(
    worksheet: Any,
    sheet_name: str,
    exported_dataframe: pd.DataFrame,
    data_additional: dict[str, pd.DataFrame],
    options: dict[str, Any],
) -> None:
    """
    Apply formatting to specific worksheet.

    :param worksheet: The worksheet to apply formatting to
    :type worksheet: Any
    :param sheet_name: The name of the sheet
    :type sheet_name: str
    :param exported_dataframe: The exported dataframe
    :type exported_dataframe: pd.DataFrame
    :param data_additional: Additional data to be saved
    :type data_additional: dict[str, pd.DataFrame]
    :param options: The selected options
    :type options: dict[str, Any]
    :return: None
    :rtype: NoneType
    """
    if options["selected_liquidation"] == "Sell In":
        sellin_format(worksheet, sheet_name, exported_dataframe, data_additional, options)
    else:
        sellout_format(worksheet, sheet_name, exported_dataframe, data_additional)

    logger.info(f"Data saved with formatting.")
