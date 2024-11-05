"""
This module contains the class to integrate the sellout dataframe.
"""

import pandas as pd

from schemas.request.options import Options


class SellOutIntegrator:
    """
    A class to assemble the sellout dataframe
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Constructor of the class.

        :param dataframe:
        :type dataframe: pd.DataFrame
        :return: None
        :rtype: NoneType
        """
        self.dataframe: pd.DataFrame = dataframe

    def filter_options(self, binnacle: pd.DataFrame, options: Options, list_month: list[int]) -> pd.DataFrame:
        """
        Filters the sellout dataframe based on the selected options.

        :param binnacle: The binnacle dataframe.
        :type binnacle: pd.DataFrame
        :param options: The options selected by the user.
        :type options: Options
        :param list_month: The list of months.
        :type list_month: List[int]
        :return: A dataframe filtered by the selected options.
        :rtype: pd.DataFrame
        """
        filtered_df = self.dataframe[
            (self.dataframe["COD_ZNJE"] == binnacle[binnacle["DES_ZNJE"] == options.nodo]["COD_ZNJE"].unique().tolist()[0]) &
            (self.dataframe["YEAR"] == int(options.year)) &
            (self.dataframe["MONTH"].isin(list_month))
        ].reset_index(drop=True).copy()
        return filtered_df

    @staticmethod
    def format_family(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the family column in the dataframe.

        :param dataframe: The dataframe to format the family column.
        :type dataframe: pd.DataFrame
        :return: The dataframe with the family column formatted.
        :rtype: pd.DataFrame
        """
        dataframe['FAMILIA'] = dataframe['FAMILIA'].apply(lambda family: family.split(' ')[1][:3].upper())
        return dataframe

    def merge_with_prices_dataframe(self, prices: pd.DataFrame) -> pd.DataFrame:
        """
        Merges the sellout dataframe with the prices dataframe.

        :param prices: The prices dataframe.
        :type prices: pd.DataFrame
        :return: A dataframe with the sellout data merged with the price data.
        :rtype: pd.DataFrame
        """
        merged_df: pd.DataFrame = self.dataframe.merge(
            prices,
            on=['COD_ZNJE', 'COD_PRODUCTO'],
            how='left'
        )
        return merged_df

    @staticmethod
    def merge_with_pivot_dataframe(merged_df: pd.DataFrame, pivot_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merges the sellout dataframe with the pivot dataframe.

        :param merged_df: The sellout dataframe.
        :type merged_df: Pd.DataFrame
        :param pivot_df: The pivot dataframe.
        :type pivot_df: Pd.DataFrame
        :return: A dataframe with the sellout data merged with the pivot data.
        :rtype: pd.DataFrame
        """
        merged_pivot_df: pd.DataFrame = merged_df.merge(
            pivot_df,
            on=['COD_ZDES', 'ETAPA', 'FAMILIA', 'COD_PRODUCTO'],
            how='inner'
        )
        return merged_pivot_df

    @staticmethod
    def add_contribution_column(columns: list[str], dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Adds contribution column to the dataframe

        :param columns: The columns to iterate
        :type columns: list[str]
        :param dataframe: The dataframe to add contribution column
        :type dataframe: pd.DataFrame
        :return: The dataframe with contribution column
        :rtype: pd.DataFrame
        """
        for application in columns[4:]:
            dataframe[f'APORTE {application}'] = dataframe['PVP'] * dataframe['CTD_SACOS'] * dataframe[application] * (
                1 if application == 'Bonif. P.Base' else dataframe['Dto. Factura']
            )
        return dataframe