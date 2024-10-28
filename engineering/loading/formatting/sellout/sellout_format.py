"""
This module contains functions to format the sellout data.
"""

import pandas as pd

from openpyxl.worksheet.worksheet import Worksheet

from engineering.loading.formatting.excel_styles import (
    header_format,
    summary_format,
    subtotal_format, columns_format,
)
from engineering.loading.formatting.utils import (
    get_cols_widths,
    get_excel_column_letter,
)
from schemas.request.options import Options


def base_sheet_format(
    dataframe: dict[str, pd.DataFrame],
    worksheet: Worksheet,
    sheet_name: str,
    options: Options
) -> None:
    """
    Apply formatting to the base sheet of sellout.

    :param dataframe: The exported dataframe
    :type dataframe: dict[str, pd.DataFrame]
    :param worksheet: The worksheet to apply formatting to
    :type worksheet: Worksheet
    :param sheet_name: The name of the sheet
    :type sheet_name: str
    :param options: The selected options
    :type options: Options
    :return: None
    :rtype: NoneType
    """
    data: pd.DataFrame = dataframe[sheet_name]
    pivot: pd.DataFrame = dataframe["pivot"]
    letter: dict[str, str] = {
        "ctd": get_excel_column_letter(data.columns.get_loc("Cantidad facturada") + 1),
        "pvp": get_excel_column_letter(data.columns.get_loc("PVP") + 1)
    }
    if "Bonif. P.Base" in list(pivot.columns):
        letter["base"] = get_excel_column_letter(data.columns.get_loc("Bonif. P.Base") + 1)
        letter["contribution_base"] = get_excel_column_letter(data.columns.get_loc("Bonif. P.Base") + 1)
        for row in range(3, len(data) + 2):
            formula = f"={letter['ctd']}{row}*{letter['base']}{row}"
            worksheet[f"{letter['contribution_base']}{row}"] = formula

    if "Bonif. P.Neto" in list(pivot.columns):
        letter["net"] = get_excel_column_letter(data.columns.get_loc("Bonif. P.Neto") + 1)
        letter["contribution_net"] = get_excel_column_letter(data.columns.get_loc("Bonif. P.Neto") + 1)
        for row in range(3, len(data) + 2):
            formula = f"={letter['ctd']}{row}*{letter['base']}{row}*{letter['net']}{row}"
            worksheet[f"{letter['contribution_net']}{row}"] = formula

    subtotal_columns: list[str] = ['TM', 'Valor neto', 'Cantidad facturada'] + [f'APORTE {applic}' for applic in list(pivot.columns)[4:]]
    subtotal_format(data, worksheet, subtotal_columns)
    header_format(data, worksheet)
    columns_format(data, worksheet)

    # col_index = data.columns.get_loc("Dto. Factura")
    # worksheet.set_column(col_index, col_index, 18, "")
    # if "Bonif. P.Base" in list(pivot.columns):
    #     worksheet.write(1, data.columns.get_loc("Bonif. P.Base") - 1, "Importe P.Base", "")
    #     col_index = data.columns.get_loc("Bonif. P.Base")
    #     worksheet.write(col_index, col_index, 18, "")
    #
    # if "Bonif. P.Neto" in list(pivot.columns):
    #     worksheet.write(1, data.columns.get_loc("Bonif. P.Neto") - 1, "Importe P.Neto", "")
    #     col_index = data.columns.get_loc("Bonif. P.Neto")
    #     worksheet.write(col_index, col_index, 18, "")

def sellout_format(
    dataframe: dict[str, pd.DataFrame],
    worksheet: Worksheet,
    sheet_name: str,
    options: Options
) -> None:
    """
    Apply formatting to specific worksheet of sellout.

    :param dataframe: The exported dataframe
    :type dataframe: pd.DataFrame
    :param worksheet: The worksheet to apply formatting to
    :type worksheet: Worksheet
    :param sheet_name: The name of the sheet
    :type sheet_name: str
    :param options: The selected options
    :type options: Options
    """
    worksheet.sheet_view.showGridLines = False
    if "Base" in sheet_name: base_sheet_format(dataframe, worksheet, sheet_name, options)
    if "Resumen" in sheet_name: summary_format(dataframe[sheet_name], worksheet)
