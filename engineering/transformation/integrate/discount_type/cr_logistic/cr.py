"""
This module contains the class to integrate the CR Logistic sellin data.
"""

import pandas as pd

from engineering.transformation.integrate.sellin import SellinIntegrator


class CrLogisticSellinIntegrator(SellinIntegrator):
    """
    A class to integrate the CR Logistic sellin data.
    """

    def __init__(self) -> None:
        super().__init__()
        self.rebate: str = ""

    @staticmethod
    def filter_ref_order(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the dataframe based on the reference order.

        :param dataframe: The dataframe to filter
        :type dataframe: pd.DataFrame
        :return: The dataframe filtered by reference order
        :rtype: pd.DataFrame
        """
        filtered_df: pd.DataFrame = dataframe[dataframe['REF_PEDIDO'].str.contains('RECOGE')]
        filtered_df.reset_index(drop=True)
        return filtered_df

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
        dataframe['APORTE'] = dataframe['TMS'] * dataframe['Bonificación'].astype(float)
        return dataframe