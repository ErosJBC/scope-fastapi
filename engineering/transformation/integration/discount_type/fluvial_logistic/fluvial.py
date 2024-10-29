"""
This module contains the class to integrate the Fluvial Logistic sellin data.
"""

import pandas as pd

from engineering.transformation.integration.sellin import SellinIntegrator


class FluvialLogisticSellinIntegrator(SellinIntegrator):
    """
    A class to integrate the Fluvial Logistic sellin data.
    """

    def __init__(self) -> None:
        super().__init__()
        self.rebate: str = ""

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
        dataframe['APORTE'] = pd.to_numeric(dataframe['APORTE'])
        return dataframe

    def add_additional_discount_column(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Adds additional discount column to the dataframe

        :param dataframe: The dataframe to add additional discount column
        :type dataframe: pd.DataFrame
        :return: The dataframe with additional discount column
        :rtype: pd.DataFrame
        """
        return dataframe

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
        return dataframe