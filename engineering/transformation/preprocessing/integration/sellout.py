"""
This module contains the SellOutAssembler class, which is responsible for integrating sellout data with the binnacle dataframe.
"""

import pandas as pd


class SellOutAssembler:
    """
    A class to integrate sellout data with the binnacle dataframe
    """

    def __init__(self) -> None:
        self.sellout: str = ""

    @staticmethod
    def filter_sellout(
        dataframe: pd.DataFrame, binnacle: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Integrate binnacle data to the sellout dataframe

        :param dataframe: The dataframe containing sellout data.
        :type dataframe: pd.DataFrame
        :param binnacle: The dataframe containing binnacle metadata.
        :type binnacle: pd.DataFrame
        :return: An integrated dataframe containing prices and SKU metadata
        :rtype: pd.DataFrame
        """
        integrated_sellout = dataframe[dataframe['COD_ZNJE'].isin(binnacle['COD_ZNJE'].unique())].copy()
        integrated_sellout.reset_index(drop=True, inplace=True)
        return integrated_sellout
