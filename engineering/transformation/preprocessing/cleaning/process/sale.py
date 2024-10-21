"""
A module for sale process in the engineering.transformation.preprocessing.cleaning.process package.
"""

import pandas as pd

from config.settings import SaleSettings


class SaleProcess:
    """
    SaleProcess process representation that requires its settings to instantiate.
    """

    def __init__(self, settings: SaleSettings):
        # self.type: str = settings.TYPE
        self.columns: list[str] = settings.COLUMNS
        self.rename_columns: list[str] = settings.RENAME_COLUMNS

    def add_columns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Adds columns to the sellout dataframe based on the given settings.

        :param dataframe: The dataframe containing sellout data.
        :type dataframe: pd.DataFrame
        :return: A dataframe with added columns.
        :rtype: pd.DataFrame
        """
        dataframe['Periodo'] = dataframe['Periodo'].astype(str)
        dataframe[['Month', 'Year']] = dataframe['Periodo'].str.split('.', expand=True)
        added_columns_df: pd.DataFrame = dataframe[['Year', 'Month'] + list(self.columns[1:])]
        return added_columns_df

    def rename_columns_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Renames the columns of the sellout dataframe based on the given settings.

        :param dataframe: The dataframe containing sellout data.
        :type dataframe: pd.DataFrame
        :return: A dataframe with renamed columns.
        :rtype: pd.DataFrame
        """
        renamed_df: pd.DataFrame = dataframe.copy()
        renamed_df.columns = self.rename_columns
        return renamed_df

    def filter_cod_znje(self, dataframe: pd.DataFrame, binnacle: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the sellout dataframe based on the ZNJE codes.

        :param dataframe: The dataframe containing sellout data.
        :type dataframe: pd.DataFrame
        :param binnacle: The dataframe containing the binnacle data.
        :type binnacle: pd.DataFrame
        :return: A dataframe filtered by ZNJE codes.
        :rtype: pd.DataFrame
        """
        filtered_df: pd.DataFrame = dataframe[dataframe['COD_ZNJE'].isin(binnacle['COD_ZNJE'].unique())]
        return filtered_df
