"""
A module for clients in the engineering.transformation.preprocessing package.
"""

import pandas as pd

from config.settings import SellOutSettings


class SellOutProcess:
    """
    SellOut process representation that requires its settings to instantiate.
    """

    def __init__(self, settings: SellOutSettings):
        self.type: str = settings.TYPE
        self.columns: list[str] = settings.COLUMNS
        self.rename_columns: list[str] = settings.RENAME_COLUMNS

    def filter_type(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the sellout dataframe based on type.

        :param dataframe: The dataframe containing sellout data.
        :type dataframe: pd.DataFrame
        :return: A dataframe filtered by type.
        :rtype: pd.DataFrame
        """
        filtered_df: pd.DataFrame = dataframe.loc[
            dataframe["Tipo"] == self.type
        ].copy()
        return filtered_df

    def add_columns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Adds columns to the sellout dataframe based on the given settings.

        :param dataframe: The dataframe containing sellout data.
        :type dataframe: pd.DataFrame
        :return: A dataframe with added columns.
        :rtype: pd.DataFrame
        """
        dataframe['Fecha'] = pd.to_datetime(dataframe['Fecha'])
        dataframe['MONTH'] = dataframe['Fecha'].dt.month
        dataframe['YEAR'] = dataframe['Fecha'].dt.year
        added_columns_df = dataframe[['MONTH', 'YEAR'] + list(self.columns[1:])]
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
