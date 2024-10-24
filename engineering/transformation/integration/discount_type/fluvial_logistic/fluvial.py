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
        return dataframe
