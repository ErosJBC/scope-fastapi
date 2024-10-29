"""
This module contains the SaleAssembler class, which is responsible for integrating sales data with clients and binnacle data.
"""

import pandas as pd

from config.settings import Settings


class SaleAssembler:
    """
    A class to assemble sales data
    """

    def __init__(self, settings: Settings):
        self.filter_columns: list[str] = settings.clients.FILTER_COLUMNS
        self.merge_columns: list[str] = settings.sales.MERGE_COLUMNS

    def merged_sales(
        self, dataframe: pd.DataFrame, clients: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge sales data with clients data

        :param dataframe: The dataframe containing sales data.
        :type dataframe: pd.DataFrame
        :param clients: The clients dataframe to merge with sales data
        :type clients: pd.DataFrame
        :return: An integrated dataframe containing prices and SKU metadata
        :rtype: pd.DataFrame
        """
        merged_sales = dataframe.merge(clients[self.filter_columns], on=self.merge_columns, how='left')
        return merged_sales

    @staticmethod
    def filter_sales(
        dataframe: pd.DataFrame, binnacle: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Integrates sales data with binnacle data

        :param dataframe: The dataframe containing prices data.
        :type dataframe: pd.DataFrame
        :param binnacle: Binnacle dataframe to filter sales data
        :type binnacle: pd.DataFrame
        :return: An integrated dataframe containing prices and SKU metadata
        :rtype: pd.DataFrame
        """
        integrated_sales = dataframe[dataframe['COD_ZNJE'].isin(binnacle['COD_ZNJE'].unique())].copy()
        integrated_sales.sort_values(by=['YEAR', 'MONTH'], inplace=True)
        integrated_sales.reset_index(drop=True, inplace=True)
        return integrated_sales
