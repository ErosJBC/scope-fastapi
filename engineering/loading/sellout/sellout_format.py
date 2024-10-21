import pandas as pd

from typing import Any

from engineering.transformation.integrate.binnacle import BinnacleIntegrator

from utils.utils import get_cols_widths, get_excel_column_letter


def base_sheet_format(
    worksheet: Any,
    dataframe: pd.DataFrame,
    data_additional: dict[str, pd.DataFrame]
) -> None:
    """
    Apply formatting to the base sheet of sellout.

    :param worksheet: The worksheet to apply formatting to
    :type worksheet: Any
    :param dataframe: The exported dataframe
    :type dataframe: pd.DataFrame
    :param data_additional: Additional data to be saved
    :type data_additional: dict[str, pd.DataFrame]
    :return: None
    :rtype: NoneType
    """

    pivot: pd.DataFrame = data_additional["pivot"]
    binnacle: pd.DataFrame = data_additional["binnacle"]
    application: str = BinnacleIntegrator.get_type_application(binnacle)
    letters: dict[str, str] = {}
    if application != "TMS":
        letters["ctd"] = get_excel_column_letter(dataframe.columns.get_loc("CTD_SACOS") + 1)
        letters["pvp"] = get_excel_column_letter(dataframe.columns.get_loc("PVP") + 1)
        if "Bonif. P.Base" in list(pivot.columns):
            letters["base"] = get_excel_column_letter(dataframe.columns.get_loc("Bonif. P.Base") + 1)
            letters["contribution_base"] = get_excel_column_letter(dataframe.columns.get_loc("Bonif. P.Base") + 1)
            for row in range(3, len(dataframe) + 2):
                formula = f"={letters['ctd']}{row}*{letters['base']}{row}"
                worksheet.write_formula(f"{letters['contribution_base']}{row}", formula)

        if "Bonif. P.Neto" in list(pivot.columns):
            letters["net"] = get_excel_column_letter(dataframe.columns.get_loc("Bonif. P.Neto") + 1)
            letters["contribution_net"] = get_excel_column_letter(dataframe.columns.get_loc("Bonif. P.Neto") + 1)
            for row in range(3, len(dataframe) + 2):
                formula = f"={letters['ctd']}{row}*{letters['base']}{row}*{letters['net']}{row}"
                worksheet.write_formula(f"{letters['contribution_net']}{row}", formula)

    for col_num, col_name in enumerate(dataframe.columns):
        col_letter = get_excel_column_letter(col_num + 1)
        formula, cell_format = (f'=SUBTOTAL(9, {col_letter}3:{col_letter}{len(dataframe) + 2})', '')\
            if col_name in ['TM', 'Valor neto', 'Cantidad facturada'] + [f'APORTE {aplic}' for aplic in list(data_additional.columns)[4:]]\
            else ('', '')
        worksheet.write(0, col_num, formula, cell_format)

    col_index = dataframe.columns.get_loc("Dto. Factura")
    worksheet.set_column(col_index, col_index, 18, "")
    if "Bonif. P.Base" in list(pivot.columns):
        worksheet.write(1, dataframe.columns.get_loc("Bonif. P.Base") - 1, "Importe P.Base", "")
        col_index = dataframe.columns.get_loc("Bonif. P.Base")
        worksheet.write(col_index, col_index, 18, "")

    if "Bonif. P.Neto" in list(pivot.columns):
        worksheet.write(1, dataframe.columns.get_loc("Bonif. P.Neto") - 1, "Importe P.Neto", "")
        col_index = dataframe.columns.get_loc("Bonif. P.Neto")
        worksheet.write(col_index, col_index, 18, "")

def summary_sheet_format(
    worksheet: Any,
    dataframe: pd.DataFrame
) -> None:
    """
    Apply formatting to the summary sheet of sellout.

    :param worksheet: The worksheet to apply formatting to
    :type worksheet: Any
    :param dataframe: The exported dataframe
    :type dataframe: pd.DataFrame
    :return: None
    :rtype: NoneType
    """
    for col_num, value in enumerate(dataframe.columns.values):
        worksheet.write(0, col_num, value, "")
    for col_num, value in enumerate(dataframe.iloc[-1]):
        worksheet.write(len(dataframe), col_num, value, "")
    for col_num, width in enumerate(get_cols_widths(dataframe)):
        worksheet.set_column(col_num, col_num, width)

def sellout_format(
    worksheet: Any,
    sheet_name: str,
    dataframe: pd.DataFrame,
    data_additional: dict[str, pd.DataFrame],
) -> None:
    """
    Apply formatting to specific worksheet of sellout.

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
    :return: None
    :rtype: NoneType
    """
    if "Base" in sheet_name:
        base_sheet_format(worksheet, dataframe, data_additional)
    else:
        summary_sheet_format(worksheet, dataframe)
