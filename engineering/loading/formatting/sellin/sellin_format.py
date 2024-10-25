"""
This module contains functions to format the sellin data.
"""

import pandas as pd

from openpyxl.worksheet.worksheet import Worksheet

from engineering.loading.formatting.excel_styles import (
    columns_format,
    header_format,
    subtotal_format,
    summary_format,
    styles,
)
from engineering.loading.formatting.utils import get_excel_column_letter
from schemas.request.options import Options


def sellin_format(
    dataframe: dict[str, pd.DataFrame],
    worksheet: Worksheet,
    sheet_name: str,
    options: Options
) -> None:
    """
    Load dataframes into an Excel file and apply formatting.

    :param dataframe: The exported dataframe
    :type dataframe: pd.DataFrame
    :param worksheet: The worksheet to apply formatting to
    :type worksheet: Worksheet
    :param sheet_name: The name of the sheet
    :type sheet_name: str
    :param options: The selected options
    :type options: Options
    """
    data = dataframe[sheet_name]
    worksheet.sheet_view.showGridLines = False
    list_columns = ['TM', 'Valor neto', 'Cantidad facturada']
    application: str = ""
    letter: dict[str, str] = {}
    if options.discount_type == "Rebate":
        if options.nodo == "D. COPACIGULF":
            if "Base" in sheet_name:
                subtotal_format(data, worksheet, list_columns)
                header_format(data, worksheet)
                columns_format(data, worksheet)

            if "Resumen" in sheet_name:
                pass
        else:
            if "Base" in sheet_name:
                list_columns += ['APORTE']
                letter["tms"] = get_excel_column_letter(data.columns.get_loc('TM') + 1)
                letter["pvp"] = get_excel_column_letter(data.columns.get_loc('PVP') + 1)
                letter["bonus"] = get_excel_column_letter(data.columns.get_loc('Bonificación') + 1)
                letter["d_vol"] = get_excel_column_letter(data.columns.get_loc('Dto. Factura') + 1)
                letter["d_adit"] = get_excel_column_letter(data.columns.get_loc('Dto. Adicional') + 1)
                column_contribution = data.shape[1]
                letter["contribution"] = get_excel_column_letter(column_contribution)

                if application == "TMS":
                    for row_num in range(3, len(data) + 2):
                        formula = f'={letter["tms"]}{row_num}*{letter["bonus"]}{row_num}'
                        worksheet[f'{letter["contribution"]}{row_num}'] = formula
                elif application == "P_BASE":
                    for row_num in range(3, len(data) + 2):
                        formula = f'={letter["tms"]}{row_num}*{letter["pvp"]}{row_num}*{letter["bonus"]}{row_num}*(1+{letter["d_vol"]}{row_num})'
                        worksheet[f'{letter["contribution"]}{row_num}'] = formula
                else:
                    for row_num in range(3, len(data) + 2):
                        formula = f'={letter["tms"]}{row_num}*{letter["pvp"]}{row_num}*{letter["bonus"]}{row_num}*(1+{letter["d_vol"]}{row_num}+{letter["d_adit"]}{row_num})'
                        worksheet[f'{letter["contribution"]}{row_num}'] = formula
                subtotal_format(data, worksheet, list_columns)
                header_format(data, worksheet)
                columns_format(data, worksheet)
                worksheet[f'{letter["contribution"]}2'] = "Importe NC"

            if "Resumen" in sheet_name: summary_format(data, worksheet)
    else:
        list_columns += ['APORTE']
        if options.discount_type.startswith("Logístico"):  # type: ignore
            if "Base" in sheet_name:
                # Aporte column will be created in the last column
                column_contribution = data.shape[1]
                letter["tms"] = get_excel_column_letter(data.columns.get_loc('TM') + 1)
                letter["bonus"] = get_excel_column_letter(data.columns.get_loc('Bonificación') + 1)
                letter["contribution"] = get_excel_column_letter(column_contribution)

                for row_num in range(3, len(data) + 2):
                    formula = f'={letter["tms"]}{row_num}*{letter["bonus"]}{row_num}'
                    worksheet[f'{letter["contribution"]}{row_num}'] = formula

                subtotal_format(data, worksheet, list_columns)
                header_format(data, worksheet)
                columns_format(data, worksheet)
                worksheet[f'{letter["contribution"]}2'] = "Importe NC"

            if "Resumen" in sheet_name: summary_format(data, worksheet)
        elif options.discount_type == "Reconocimiento Comercial":
            if "Base" in sheet_name:
                letter["tms"] = get_excel_column_letter(data.columns.get_loc('TM') + 1)
                letter["ctd"] = get_excel_column_letter(data.columns.get_loc('Cantidad facturada') + 1)
                letter["pvp"] = get_excel_column_letter(data.columns.get_loc('PVP') + 1)
                letter["bonus"] = get_excel_column_letter(data.columns.get_loc('Bonificación') + 1)
                letter["d_vol"] = get_excel_column_letter(data.columns.get_loc('Dto. Factura') + 1)
                letter["credit"] = get_excel_column_letter(data.columns.get_loc('P. Crédito') + 1)
                letter["d_adit"] = get_excel_column_letter(data.columns.get_loc('Dto. Adicional') + 1)
                letter["contribution"] = get_excel_column_letter(data.columns.get_loc('APORTE') + 1)

                if application == "TMS":
                    for row_num in range(3, len(data) + 2):
                        formula = f'={letter["tms"]}{row_num}*{letter["bonus"]}{row_num}'
                        worksheet[f'{letter["contribution"]}{row_num}'] = formula
                elif application == "P_BASE":
                    for row_num in range(3, len(data) + 3):
                        formula = f'=TRUNC({letter["pvp"]}{row_num}*(1+{letter["d_vol"]}{row_num}-{letter["bonus"]}{row_num}),3)'
                        worksheet[f'{letter["credit"]}{row_num}'] = formula

                    for row_num in range(3, len(data) + 3):
                        formula = f'=TRUNC({letter["pvp"]}{row_num}*{letter["bonus"]}{row_num},3)*{letter["ctd"]}{row_num}*(1+{letter["d_adit"]}{row_num})'
                        worksheet[f'{letter["contribution"]}{row_num}'] = formula
                else:
                    for row_num in range(3, len(data) + 3):
                        formula = f'=TRUNC({letter["pvp"]}{row_num}*(1+{letter["d_vol"]}{row_num}),3)'
                        worksheet[f'{letter["credit"]}{row_num}'] = formula

                    for row_num in range(3, len(data) + 3):
                        formula = f'={letter["pvp"]}{row_num}*(1+{letter["d_adit"]}{row_num})*{letter["bonus"]}{row_num}*{letter["ctd"]}{row_num}'
                        worksheet[f'{letter["contribution"]}{row_num}'] = formula

                subtotal_format(data, worksheet, list_columns)
                header_format(data, worksheet)
                columns_format(data, worksheet)

            if "Resumen" in sheet_name: summary_format(data, worksheet)
