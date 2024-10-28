"""
Module to integrate the binnacle dataframe.
"""

import pandas as pd

from typing import Any
from pydantic import PositiveInt

from schemas.request.options import Options


class BinnacleIntegrator:
    """
    Class to integrate the binnacle dataframe.
    """

    def __init__(self) -> None:
        self.binnacle: str = ""

    @staticmethod
    def filter_options(dataframe: pd.DataFrame, options: Options) -> pd.DataFrame:
        """
        Filters the binnacle dataframe based on options.

        :param dataframe: The dataframe containing binnacle data.
        :type dataframe: pd.DataFrame
        :param options: The options to filter the dataframe.
        :type options: dict[str, Any]
        :return: A dataframe filtered by options.
        :rtype: pd.DataFrame
        """
        filtered_df: pd.DataFrame = dataframe[
            (dataframe['SI/SO'] == options.liquidation) & (dataframe['DES_ZNJE'] == options.nodo) &
            (dataframe['TIPO_DESCUENTO'] == options.discount_type)
        ]
        return filtered_df

    @staticmethod
    def overwrite_family(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Overwrites the family column in the binnacle dataframe.

        :param dataframe: The dataframe containing binnacle data.
        :type dataframe: pd.DataFrame
        :return: A dataframe with the family column overwritten.
        :rtype: Pd.DataFrame
        """
        dataframe['FAMILIA'] = dataframe['FAMILIA'].apply(lambda family: str(family).split(" ")[1][:3].upper())
        return dataframe

    @staticmethod
    def create_lower_tm_column(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Create the lower TM column in the binnacle dataframe.

        :param dataframe: The dataframe containing binnacle data.
        :type dataframe: pd.DataFrame
        :return: A dataframe with the lower TM column.
        :rtype: pd.DataFrame
        """
        dataframe['LOWER_TM'] = dataframe['CONDICION'].str.split(' - ').str[0].str.replace('K', '').astype(float) * 1000
        return dataframe

    @staticmethod
    def create_upper_tm_column(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Create the upper TM column in the binnacle dataframe.

        :param dataframe: The dataframe containing binnacle data.
        :type dataframe: pd.DataFrame
        :return: A dataframe with the upper TM column.
        :rtype: pd.DataFrame
        """
        dataframe['UPPER_TM'] = dataframe['CONDICION'].str.split(' - ').str[1].str.split(' ').str[0].str.replace('K', '').astype(float) * 1000
        return dataframe

    @staticmethod
    def create_mean_tm_column(dataframe: pd.DataFrame, filtered_sellin: pd.DataFrame) -> pd.DataFrame:
        """
        Create the mean TM column in the binnacle dataframe.

        :param dataframe: The dataframe containing binnacle data.
        :type dataframe: pd.DataFrame
        :param filtered_sellin: The filtered sellin dataframe.
        :type filtered_sellin: pd.DataFrame
        :return: A dataframe with the mean TM column.
        :rtype: pd.DataFrame
        """
        dataframe['MEAN_TM'] = float(filtered_sellin[["MONTH", "TMS"]].groupby(["MONTH"])["TMS"].sum().mean())
        return dataframe

    @staticmethod
    def filter_tm(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filter the binnacle dataframe based on the TM values.

        :param dataframe: The dataframe containing binnacle data.
        :type dataframe: pd.DataFrame
        :return: A dataframe filtered by TM values.
        :rtype: pd.DataFrame
        """
        filtered_df: pd.DataFrame = dataframe.loc[
            (dataframe["MEAN_TM"] >= dataframe["LOWER_TM"]) & (dataframe["MEAN_TM"] <= dataframe["UPPER_TM"])
        ].copy()
        return filtered_df

    @staticmethod
    def get_type_application(dataframe: pd.DataFrame) -> str:
        """
        Determine the application of the filtered binnacle

        :param dataframe: The filtered binnacle dataframe
        :type dataframe: pd.DataFrame
        :return: The application of the filtered binnacle
        :rtype: str
        """
        type_application: str = dataframe['APLICACION'].unique().tolist()[0]
        type_application = 'TMS' if type_application == 'Tonelada' \
            else 'P_BASE' if type_application == 'Precio Base' \
            else 'VALOR_NETO'
        return type_application

    @staticmethod
    def get_list_month_by_period(dataframe: pd.DataFrame, selected_month: str) -> list[str]:
        """
        Get the list of months based on the period of the filtered binnacle

        :param dataframe: The filtered binnacle dataframe
        :type dataframe: pd.DataFrame
        :param selected_month: The selected month
        :type selected_month: str
        :return: The list of months
        :rtype: list[str]
        """
        period = dataframe['PERIODO'].unique().tolist()[0]
        period_dict: dict[str, PositiveInt] = {'Mensual': 1, 'Bimensual': 2, 'Trimestral': 3}

        list_month_temp: list[int] = list(range(1, int(selected_month) + 1))[-period_dict[period]:]
        list_month = [str(month) for month in list_month_temp]
        return list_month

    @staticmethod
    def create_validators_column(
        binnacle: pd.DataFrame,
        sellin_sellout: pd.DataFrame,
        is_sellout: bool = False
    ) -> pd.DataFrame:
        """
        Generate the dataframe with the validators

        :param binnacle: The filtered binnacle dataframe
        :type binnacle: pd.DataFrame
        :param sellin_sellout: The filtered sellin or sellout dataframe
        :type sellin_sellout: pd.DataFrame
        :param is_sellout: A flag to determine if the dataframe is sellout
        :type is_sellout: bool
        :return: The dataframe with the validators
        :rtype: pd.DataFrame
        """
        validators: list[str] = ['COD_ZDES', 'COD_ZDEM', 'ETAPA', 'FAMILIA', 'COD_PRODUCTO']
        if is_sellout: validators.remove('COD_ZDEM')
        validators_df: pd.DataFrame = binnacle.copy()
        for index, column in enumerate(validators):
            expanded = []
            for _, row in validators_df.iterrows():
                if row[column] == 'Todo':
                    posibles = sellin_sellout.copy()
                    for val_col in validators[:index]:
                        posibles = posibles[posibles[val_col] == row[val_col]]
                    posibles = posibles[column].unique()
                    if len(posibles) > 0:
                        for item in posibles:
                            new_row = row.copy()
                            new_row[column] = item
                            expanded.append(new_row)
                else:
                    expanded.append(row)
            validators_df = pd.DataFrame(expanded)
        return validators_df

    @staticmethod
    def pivot_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Pivots the binnacle dataframe.

        :param dataframe: The dataframe containing binnacle data.
        :type dataframe: pd.DataFrame
        :return: A dataframe generated by pivoting the binnacle data.
        :rtype: pd.DataFrame
        """
        dataframe['VALOR'] = pd.to_numeric(dataframe['VALOR'].apply(
            lambda x: str(x).replace("$", "").replace(",", "")
        ))
        pivot_df: pd.DataFrame = dataframe.pivot_table(
            index=['COD_ZDES', 'ETAPA', 'FAMILIA', 'COD_PRODUCTO'], # Columns to keep as index
            columns='APLICACION', # Column to pivot
            values='VALOR', # Values to fill the pivot
            aggfunc='sum', # Aggregation function
            fill_value=0 # Fill NaN values with 0
        ).reset_index()
        pivot_df.rename(
            columns={
                'Precio Base': 'Bonif. P.Base',
                'Precio Neto': 'Bonif. P.Neto'
            },
            inplace=True
        )
        print("Pivot")
        print(pivot_df.head())
        print(pivot_df.dtypes)
        return pivot_df