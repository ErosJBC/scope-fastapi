"""
This module contains the utilities for filtering and generating the data based on the options provided.
"""

import pandas as pd
from typing import Any

from config.settings import settings
from engineering.engineering import run_process_data
from engineering.extraction.extraction import read_to_parquet
from schemas.request.options import Options


def generate_filtered_options(options: Options) -> dict[str, Any]:
    """
    Filter the options based on the selected options.

    :param options: The selected options
    :type options: Options
    :return: The filtered options
    :rtype: dict[str, Any]
    """
    dict_dataframes: dict[str, pd.DataFrame] = read_to_parquet(settings)

    binnacle: pd.DataFrame = dict_dataframes["binnacle"]
    sellin: pd.DataFrame = dict_dataframes["sales"]
    sellout: pd.DataFrame = dict_dataframes["sellout"]
    sales: pd.DataFrame = sellin if options.liquidation == "Sell In" else sellout
    filtered_options: dict[str, Any] = {}

    filtered_binnacle = binnacle[(binnacle['SI/SO'] == options.liquidation) & (binnacle['COD_ZNJE'].isin(sellin['COD_ZNJE'].unique()))]
    filtered_sales = sales[(sales['COD_ZNJE'].isin(filtered_binnacle['COD_ZNJE'].unique()))]

    filtered_options["nodo"] = [
        { "label": nodo, "value": nodo } for nodo in filtered_binnacle["DES_ZNJE"].unique()
    ]

    if options.nodo is not None:
        filtered_binnacle = filtered_binnacle[filtered_binnacle["DES_ZNJE"] == options.nodo]
        filtered_sales = filtered_sales[filtered_sales["COD_ZNJE"] == filtered_binnacle["COD_ZNJE"].unique()[0]]

    filtered_options["discount_type"] = [
        { "label": discount, "value": discount } for discount in filtered_binnacle["TIPO_DESCUENTO"].unique()
    ]

    filtered_options["year"] = [
        { "label": year, "value": year } for year in filtered_sales["YEAR"].astype(str).unique()
    ]

    if options.year is not None:
        filtered_sales = filtered_sales[filtered_sales["YEAR"] == int(options.year)]

    filtered_options["month"] = [
        { "label": month, "value": month } for month in filtered_sales["MONTH"].astype(str).unique()
    ]

    return filtered_options

def generate_excel_file(options: Options) -> dict[str, str]:
    """
    Generate the Excel file based on the selected options.

    :param options: The selected options
    :type options: Options
    :return: The file name
    :rtype: str
    """
    dict_dataframes: dict[str, pd.DataFrame] = read_to_parquet(settings)
    file_name, file_base64 = run_process_data(dict_dataframes, settings, options)
    return { "file_name": file_name, "file_base64": file_base64 }
