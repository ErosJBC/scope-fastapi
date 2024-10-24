"""
This module is used to generate the summary sheet for the rebate, fluvial logistic, commercial recognition and sellout reports
"""

import pandas as pd

from typing import Any

from constants.constants import constants
from schemas.request.options import Options


def generate_summary_rebate_sheet(
    sellin: pd.DataFrame,
    binnacle: pd.DataFrame,
    options: Options,
) -> dict[str, pd.DataFrame]:

    """
    Generate the summary sheet for the rebate report

    :param sellin: The sell in data
    :type sellin: pd.DataFrame
    :param binnacle: The binnacle data
    :type binnacle: pd.DataFrame
    :param options: The options selected by the user
    :type options: dict[str, Any]
    :return: The summary sheet for the rebate report
    :rtype: dict[str, pd.DataFrame]
    """
    cols_to_aggregate = { 'TMS': 'sum', 'VALOR_NETO': 'sum' }
    if options.nodo == "D. COPACIGULF": cols_to_aggregate.update({'APORTE': 'sum'})
    summary_sheet: pd.DataFrame = sellin.groupby('MONTH').agg(cols_to_aggregate).reset_index()
    if options.nodo == "D. COPACIGULF":
        summary_sheet["MONTH"] = summary_sheet["MONTH"].replace(constants.MONTHS)
        value = binnacle["VALOR"].unique().tolist()[0] if binnacle is not None else 0

        summary_sheet.loc["TOTAL", "MONTH"] = "Promedio VN"
        summary_sheet.loc["BASE", "TMS"] = 8000
        summary_sheet.loc["BASE", "MONTH"] = 'Base'
        summary_sheet.loc["EXCEDENTE", "MONTH"] = 'Tm excedentes'
        summary_sheet.loc["%", 'TMS'] = value * 100
        summary_sheet.loc["%", "MONTH"] = '%_Ganado'
        summary_sheet.fillna("", inplace=True)
        summary_sheet.columns = ["Mes Resumen", "Toneladas", "Dólares"]
    else:
        summary_sheet.columns = ["Mes Resumen", "Toneladas", "Dólares", "Importe NC"]
        summary_sheet.loc['TOTAL', 'Toneladas'] = summary_sheet['Toneladas'].sum()
        summary_sheet.loc['TOTAL', 'Dólares'] = summary_sheet['Dólares'].sum()
        summary_sheet.loc['TOTAL', 'Importe NC'] = summary_sheet['Importe NC'].sum()
        summary_sheet.loc['TOTAL', 'Mes Resumen'] = 'Total'

    summary_dict: dict[str, pd.DataFrame] = {"Resumen": summary_sheet}
    return summary_dict

def generate_summary_cr_fluvial_logistic_sheet(sellin: pd.DataFrame) -> dict[str, pd.DataFrame]:

    """
    Generate the summary sheet for the fluvial logistic report

    :param sellin: The sell in data
    :type sellin: pd.DataFrame
    :return: The summary sheet for the fluvial logistic report
    :rtype: dict[str, pd.DataFrame]
    """
    cols_to_aggregate = { 'TMS': 'sum', 'VALOR_NETO': 'sum', 'APORTE': 'sum' }
    summary_sheet: pd.DataFrame = sellin.groupby('DES_ZDEM').agg(cols_to_aggregate).reset_index()
    summary_sheet.columns = ["DESTINATARIO", "TMS", "USD", "APORTE"]
    summary_sheet.loc['TOTAL', 'TMS'] = summary_sheet['TMS'].sum()
    summary_sheet.loc['TOTAL', 'USD'] = summary_sheet['USD'].sum()
    summary_sheet.loc['TOTAL', 'APORTE'] = summary_sheet['APORTE'].sum()
    summary_sheet.loc['TOTAL', 'DESTINATARIO'] = 'Total'

    summary_dict: dict[str, pd.DataFrame] = {"Resumen": summary_sheet}
    return summary_dict

def generate_summary_commercial_recognition_sheet(sellin: pd.DataFrame) -> dict[str, pd.DataFrame]:

    """
    Generate the summary sheet for the commercial recognition report

    :param sellin: The sell in data
    :type sellin: pd.DataFrame
    :return: The summary sheet for the commercial recognition report
    :rtype: dict[str, pd.DataFrame]
    """
    cols_to_aggregate = { 'TMS': 'sum', 'VALOR_NETO': 'sum', 'APORTE': 'sum' }
    summary_sheet: pd.DataFrame = sellin.groupby(['MONTH', 'DES_ZDEM']).agg(cols_to_aggregate).reset_index()
    summary_sheet['MONTH'] = summary_sheet['MONTH'].replace(constants.MONTHS)
    summary_sheet.columns = ['MES', 'CLIENTE', 'TMS', 'USD', 'APORTE']
    summary_sheet.loc['TOTAL', 'TMS'] = summary_sheet['TMS'].sum()
    summary_sheet.loc['TOTAL', 'USD'] = summary_sheet['USD'].sum()
    summary_sheet.loc['TOTAL', 'APORTE'] = summary_sheet['APORTE'].sum()
    summary_sheet.loc['TOTAL', 'MES'] = 'Total'
    summary_sheet.fillna('', inplace=True)

    summary_dict: dict[str, pd.DataFrame] = {"Resumen": summary_sheet}
    return summary_dict

def generate_summary_sellout_sheet(binnacle: pd.DataFrame, sellout: pd.DataFrame, pivot: pd.DataFrame) -> dict[str, pd.DataFrame]:
    summary_sheet: pd.DataFrame
    if binnacle['APLICACION'].nunique() == 1:
        summary_sheet = sellout.groupby('DES_ZDES').agg(
            {'CTD_SACOS': 'sum', 'TMS': 'sum', f'APORTE {pivot.columns[-1]}': 'sum'}
        ).reset_index()
    else:
        summary_sheet = sellout.groupby('DES_ZDES').agg(
            {'CTD_SACOS': 'sum', 'TMS': 'sum', f'APORTE {pivot.columns[-2]}': 'sum', f'APORTE {pivot.columns[-1]}': 'sum'}
        ).reset_index()

    summary_sheet.rename(
        columns={'CTD_SACOS': 'Cantidad sacos', 'DES_ZDES': 'CLIENTE', 'TMS': 'Toneladas'},
        inplace=True
    )
    summary_sheet.loc['TOTAL', 'Toneladas'] = summary_sheet['Toneladas'].sum()
    summary_sheet.loc['TOTAL', 'Cantidad sacos'] = summary_sheet['Cantidad sacos'].sum()

    if 'Bonif. P.Base' in list(pivot.columns):
        summary_sheet.loc['TOTAL', 'APORTE Bonif. P.Base'] = summary_sheet['APORTE Bonif. P.Base'].sum()
    if 'Bonif. P.Neto' in list(pivot.columns):
        summary_sheet.loc['TOTAL', 'APORTE Bonif. P.Neto'] = summary_sheet['APORTE Bonif. P.Neto'].sum()
    summary_sheet.loc['TOTAL', 'CLIENTE'] = 'Total'

    summary_dict: dict[str, pd.DataFrame] = {"Resumen": summary_sheet}
    return summary_dict