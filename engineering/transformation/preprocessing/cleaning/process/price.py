"""
A module for clients in the engineering.transformation.preprocessing package.
"""

import pandas as pd

from config.settings import PriceSettings


class PriceProcess:
    """
    Price process representation that requires its settings to instantiate
    the consider, status sku and rename columns.
    """

    def __init__(self, settings: PriceSettings):
        self.consider: str = settings.CONSIDER
        self.status_sku: str = settings.STATUS_SKU
        self.columns: list[str] = settings.COLUMNS
        self.rename_columns: list[str] = settings.RENAME_COLUMNS

    def filter_status_sku(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the price dataframe based on status sku.

        :param dataframe: The dataframe contains price data.
        :type dataframe: pd.DataFrame
        :return: A dataframe filtered by status sku.
        :rtype: pd.DataFrame
        """
        filtered_df: pd.DataFrame = dataframe[
            dataframe["Status SKU"] == self.status_sku
        ].copy()
        return filtered_df

    def filter_consider(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the price dataframe based on considering.

        :param dataframe: The dataframe containing price data.
        :type dataframe: pd.DataFrame
        :return: A dataframe filtered by consider.
        :rtype: pd.DataFrame
        """
        filtered_df: pd.DataFrame = dataframe[
            dataframe["Considerar"] == self.consider
        ].copy()
        return filtered_df

    def rename_columns_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Rename the binnacle dataframe.

        :param dataframe: The dataframe containing binnacle data.
        :type dataframe: pd.DataFrame
        """
        renamed_df = dataframe[self.columns[2:]].copy()
        renamed_df.columns = self.rename_columns
        return renamed_df
