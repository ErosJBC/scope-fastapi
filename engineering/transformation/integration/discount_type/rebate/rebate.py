"""
This module contains the class to integrate rebate with sellin data
"""

import pandas as pd

from engineering.transformation.integration.sellin import SellinIntegrator


class RebateSellinIntegrator(SellinIntegrator):
    """
    A class to integrate rebate with sellin data
    """

    def __init__(self) -> None:
        super().__init__()
        self.rebate: str = ""

    def add_additional_discount_column(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Adds additional discount column to the dataframe

        :param dataframe: The dataframe to add additional discount column
        :type dataframe: pd.DataFrame
        :return: The dataframe with additional discount column
        :rtype: pd.DataFrame
        """
        dataframe['Dto. Adicional'] = (-1 *
            (dataframe['PVP'] * (dataframe['P_BASE'] - dataframe['VALOR_NETO'] + dataframe['D_VOL'])/dataframe['P_BASE'])/dataframe['P. Crédito']
        )
        return dataframe

    def add_credit_column(self, dataframe: pd.DataFrame, type_application: str = "TMS") -> pd.DataFrame:
        """
        Adds credit column to the dataframe

        :param dataframe: The dataframe to add credit column
        :type dataframe: pd.DataFrame
        :param type_application: The type of application to calculate credit
        :type type_application: str
        :return: The dataframe with credit column
        :rtype: pd.DataFrame
        """
        dataframe["P. Crédito"] = dataframe['PVP'] * (1 + dataframe['Dto. Factura'])
        return dataframe

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
        if type_application == "TMS":
            dataframe['APORTE'] = dataframe['TMS'] * dataframe['Bonificación'].astype(float)
        elif type_application == "P_BASE":
            dataframe['APORTE'] = (dataframe['P_BASE'] * dataframe['Bonificación'].astype(float) *
                (1 + dataframe['D_CONT'] / (dataframe['P_BASE'] + dataframe['D_VOL']))
            )
        else:
            dataframe['APORTE'] = (dataframe['P_BASE'] + dataframe['D_VOL']) * dataframe['Bonificación'].astype(float)
        return dataframe
