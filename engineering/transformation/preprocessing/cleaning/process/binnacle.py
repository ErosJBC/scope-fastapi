"""
A module for clients in the engineering.transformation.preprocessing package.
"""

import pandas as pd

from config.settings import BinnacleSettings


class BinnacleProcess:
    """
    Binnacle process representation that requires its settings to instantiate
    the status, via and rename columns.
    """

    def __init__(self, settings: BinnacleSettings):
        self.status: str = settings.STATUS
        self.via: str = settings.VIA
        self.columns: list[str] = settings.COLUMNS
        self.rename_columns: list[str] = settings.RENAME_COLUMNS

    def filter_status(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the binnacle dataframe based on status.

        :param dataframe: The dataframe containing binnacle data.
        :type dataframe: pd.DataFrame
        :return: A dataframe filtered by status.
        :rtype: pd.DataFrame
        """
        filtered_df: pd.DataFrame = dataframe.loc[
            dataframe["Status"] == self.status
        ].copy()
        return filtered_df

    def filter_via(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the binnacle dataframe based on via.

        :param dataframe: The dataframe containing binnacle data.
        :type dataframe: pd.DataFrame
        :return: A dataframe filtered by via.
        :rtype: pd.DataFrame
        """
        filtered_df: pd.DataFrame = dataframe.loc[
            dataframe["Vía"] == self.via
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
