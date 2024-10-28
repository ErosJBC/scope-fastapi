"""
This module contains the class to integrate the sellin dataframe.
"""

from abc import ABC, abstractmethod

import pandas as pd

from schemas.request.options import Options


class SellinIntegrator(ABC):
    """
    A class to assemble the sellin dataframe
    """

    def __init__(self) -> None:
        self.sellin: str = ""

    @staticmethod
    def filter_options(dataframe: pd.DataFrame, options: Options, months: list[str]) -> pd.DataFrame:
        """
        Filters the sellout dataframe based on the selected options.

        :param dataframe: The dataframe contains sellout data.
        :type dataframe: pd.DataFrame
        :param options: The options selected by the user.
        :type options: Options
        :param months: The list of months to filter the dataframe.
        :type months: list[str]
        :return: A dataframe filtered by the selected options.
        :rtype: pd.DataFrame
        """
        filtered_df: pd.DataFrame = dataframe[
            (dataframe['DES_ZNJE'] == options.nodo) &
            (dataframe['YEAR'] == int(options.year)) &  # type: ignore
            (dataframe['MONTH'].isin([int(month) for month in months])) &
            (dataframe['CLASE_FACTURA'].isin(['ZF01', 'ZNC7']))
            ]
        return filtered_df

    @staticmethod
    def merge_dataframes(dataframe: pd.DataFrame, binnacle: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the binnacle dataframe based on options.

        :param dataframe: The dataframe containing selling data.
        :type dataframe: pd.DataFrame
        :param binnacle: The dataframe containing binnacle data.
        :type binnacle: pd.DataFrame
        :return: A dataframe filtered by options.
        :rtype: pd.DataFrame
        """
        dataframe['COD_ZDES'] = dataframe['COD_ZDES'].astype(str)
        dataframe['COD_ZDEM'] = dataframe['COD_ZDEM'].astype(str)
        binnacle['COD_ZDES'] = binnacle['COD_ZDES'].astype(str)
        binnacle['COD_ZDEM'] = binnacle['COD_ZDEM'].astype(str)
        merged_df: pd.DataFrame = dataframe.merge(
            binnacle[['COD_ZDES', 'COD_ZDEM', 'ETAPA', 'FAMILIA', 'COD_PRODUCTO', 'VALOR']].drop_duplicates(),
            how="inner"
        )
        merged_df.rename(columns={'VALOR': 'Bonificación'}, inplace=True)
        return merged_df

    @staticmethod
    def add_pvp_column(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Adds PVP column to the dataframe

        :param dataframe: The dataframe to add PVP column
        :type dataframe: pd.DataFrame
        :return: The dataframe with PVP column
        :rtype: pd.DataFrame
        """
        dataframe["PVP"] = dataframe["P_BASE"] / dataframe["TMS"]
        dataframe["PVP"] = dataframe.apply(lambda row: row["PVP"] / 40 if row["FAMILIA"] != "Nicovita Origin" else row["PVP"] / 100, axis=1)
        return dataframe

    @staticmethod
    def add_discount_column(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Adds discount column to the dataframe

        :param dataframe: The dataframe to add discount column
        :type dataframe: pd.DataFrame
        :return: The dataframe with discount column
        :rtype: pd.DataFrame
        """
        dataframe["Dto. Factura"] = dataframe['D_VOL'] / dataframe['P_BASE']
        return dataframe

    @abstractmethod
    def add_additional_discount_column(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Adds additional discount column to the dataframe

        :param dataframe: The dataframe to add additional discount column
        :type dataframe: pd.DataFrame
        :return: The dataframe with additional discount column
        :rtype: pd.DataFrame
        """
        pass

    @abstractmethod
    def add_credit_column(self, dataframe: pd.DataFrame, type_application: str) -> pd.DataFrame:
        """
        Adds credit column to the dataframe

        :param dataframe: The dataframe to add credit column
        :type dataframe: pd.DataFrame
        :param type_application: The type of application to calculate credit
        :type type_application: str
        :return: The dataframe with credit column
        :rtype: pd.DataFrame
        """
        pass

    @abstractmethod
    def add_contribution_column(self, dataframe: pd.DataFrame, type_application: str = "TMS") -> pd.DataFrame:
        """
        Adds contribution column to the dataframe

        :param dataframe: The dataframe to add contribution column
        :type dataframe: pd.DataFrame
        :param type_application: The type of application to calculate contribution
        :type type_application: str
        :return: The dataframe with contribution column
        :rtype: pd.DataFrame
        """
        pass
