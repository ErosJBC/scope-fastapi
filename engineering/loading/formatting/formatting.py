"""
A module for formatting in the engineering.loading.formatting package.
"""

import pandas as pd
from pydantic import FilePath
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from engineering.loading.formatting.sellin.sellin_format import sellin_format
from engineering.loading.formatting.sellout.sellout_format import sellout_format
from schemas.request.options import Options


def format_worksheet(
    data: dict[str, pd.DataFrame],
    path: FilePath,
    options: Options
) -> None:
    """
    Apply formatting to specific worksheet.

    :param data: A dictionary with keys as sheet names and values as dataframes.
    :type data: dict[str, pd.DataFrame]
    :param path: The file path of the Excel file
    :type path: FilePath
    :param options: The selected options
    :type options: dict[str, Any]
    :return: None
    :rtype: NoneType
    """
    workbook: Workbook = load_workbook(path)
    worksheet: Worksheet
    for sheet_name in data:
        worksheet = workbook[sheet_name]
        if options.liquidation == "Sell In":
            sellin_format(data, worksheet, sheet_name, options)
        else:
            sellout_format(data, worksheet, sheet_name, options)
    workbook.save(path)
