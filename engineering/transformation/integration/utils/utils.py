"""
This module contains the functions to generate the sheets for the sell in report
"""

import pandas as pd

from constants.constants import constants
from schemas.request.options import Options


def generate_base_months_sheets(
    sales: pd.DataFrame,
    options: Options,
    list_month: list[int]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the sell in report

    :param sales: The sales in data
    :type sales: pd.DataFrame
    :param options: The options selected by the user
    :type options: Options
    :param list_month: The list of months to generate the sheets
    :type list_month: list[int]
    :return: The sheets for the sell in report
    :rtype: dict[str, pd.DataFrame]
    """
    sheets: dict[str, pd.DataFrame] = {}
    sheet_name: str
    if options.discount_type.startswith("Logístico"):  # type: ignore
        list_month = [int(options.month)]  # type: ignore

    columns_to_drop = ['YEAR', 'MONTH', 'COD_ZNJE', 'DES_ZNJE', 'P_BASE', 'D_VOL', 'D_COT', 'D_CONT', 'D_LOG', 'R_LOG', 'NCF', 'P_NETO']
    if options.nodo != "D. COPACIGULF":
        columns_to_drop = columns_to_drop + ['CLASE_FACTURA', 'SOCIOS']

    for month in list_month:
        sheet_name = 'Base {}.{}'.format(month if month > 9 else f'0{month}', options.year)
        df_export: pd.DataFrame = sales.loc[sales['MONTH'] == month].copy()
        df_export.drop(columns=columns_to_drop, axis=1, inplace=True)
        df_export['FECHA'] = pd.to_datetime(df_export['FECHA']).dt.strftime('%d/%m/%Y')
        df_export['COD_ZDES'] = pd.to_numeric(df_export['COD_ZDES'], downcast="integer")
        df_export['COD_PRODUCTO'] = pd.to_numeric(df_export['COD_PRODUCTO'], downcast="integer")
        df_export['COD_ZDEM'] = pd.to_numeric(df_export['COD_ZDEM'], downcast="integer")
        df_export.rename(columns=constants.COLUMNS_DATAFRAME, inplace=True)
        sheets[sheet_name] = df_export
    return sheets

def generate_base_zdes_sheets(
    sales: pd.DataFrame
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the sell in report

    :param sales: The sales in data
    :type sales: pd.DataFrame
    :return: The sheets for the sell in report
    :rtype: dict[str, pd.DataFrame]
    """
    sheets: dict[str, pd.DataFrame] = {}
    sheet_name: str
    for zdes in sales['COD_ZDES'].unique():
        sheet_name = 'Base {}'.format(sales[sales['COD_ZDES'] == zdes]['DES_ZDES'].unique()[0])
        df_export = sales.loc[sales['COD_ZDES'] == zdes].copy()
        df_export.drop(['YEAR', 'MONTH'], axis=1, inplace=True)
        df_export['FECHA'] = pd.to_datetime(df_export['FECHA']).dt.strftime('%d/%m/%Y')
        df_export.rename(columns=constants.COLUMNS_DATAFRAME, inplace=True)
        sheets[sheet_name] = df_export

    return sheets
