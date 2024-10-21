import pandas as pd

from typing import Any

from constants.constants import constants

def generate_base_months_sheets(
    sales: pd.DataFrame,
    options: dict[str, Any]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the sell in report

    :param sales: The sales in data
    :type sales: pd.DataFrame
    :param options: The options selected by the user
    :type options: dict[str, Any]
    :return: The sheets for the sell in report
    :rtype: dict[str, pd.DataFrame]
    """
    sheets: dict[str, pd.DataFrame] = {}
    if options["selected_liquidation"] == "Sell In":
        for month in options["list_months"]:
            sheet_name: str = 'Base {}.{}'.format(month if int(month) > 9 else '0' + month, options['year'])
            export_df: pd.DataFrame = sales.loc[sales['MONTH'] == month].copy()
            columns_to_drop = ['YEAR', 'MONTH', 'COD_ZNJE', 'DES_ZNJE', 'P_BASE', 'D_VOL', 'D_COT', 'D_CONT', 'D_LOG', 'R_LOG', 'NCF', 'P_NETO', 'CLASE_FACTURA', 'SOCIOS']
            export_df.drop(
                columns=columns_to_drop[:-2] if options["nodo"] == "D. COPACIGULF" else columns_to_drop,
                axis=1, inplace=True
            )
            export_df['FECHA'] = pd.to_datetime(export_df['FECHA']).dt.strftime('%d/%m/%Y')
            export_df.rename(columns=constants.COLUMNS_DATAFRAME, inplace=True)
            sheets[sheet_name] = export_df
    else:
        for zdes in sales['COD_ZDES'].unique():
            sheet_name: str = 'Base {}'.format(sales[sales['COD_ZDES'] == zdes]['DES_ZDES'].unique()[0])
            df_export = sales.loc[sales['COD_ZDES'] == zdes].copy()
            df_export.drop(['YEAR', 'MONTH'], axis=1, inplace=True)
            df_export['FECHA'] = pd.to_datetime(df_export['FECHA']).dt.strftime('%d/%m/%Y')
            df_export.rename(columns=constants.COLUMNS_DATAFRAME, inplace=True)
            sheets[sheet_name] = df_export
    return sheets
