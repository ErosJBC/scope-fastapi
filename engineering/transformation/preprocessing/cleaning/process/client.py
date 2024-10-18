"""
A module for clients in the engineering.transformation.preprocessing package.
"""

import pandas as pd

from config.settings import ClientSettings


class ClientProcess:
    """
    Client process representation that requires its settings to instantiate
    the countries.
    """

    def __init__(self, settings: ClientSettings):
        self.desc_country: list[str] = settings.DES_PAIS
        self.filter_columns: list[str] = settings.FILTER_COLUMNS

    def filter_countries(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the clients dataframe based on country codes.

        :param dataframe: The dataframe containing client data.
        :type dataframe: pd.DataFrame
        :return: A dataframe filtered by country codes.
        :rtype: pd.DataFrame
        """
        filtered_df: pd.DataFrame = dataframe.loc[
            dataframe["DES_PAIS"].isin(self.desc_country), self.filter_columns
        ].copy()
        return filtered_df
