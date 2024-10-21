"""
This module contains the class to integrate the Commercial Recognition sellin data.
"""

import pandas as pd

from engineering.transformation.integrate.sellin import SellinIntegrator
from utils.utils import trunc_number


class CommercialRecognitionSellinIntegrator(SellinIntegrator):
    """
    Class to integrate the Commercial Recognition sellin data.
    """

    def __init__(self) -> None:
        super().__init__()
        self.rebate: str = ""

    def add_credit_column(self, dataframe: pd.DataFrame, type_application: str) -> pd.DataFrame:
        """
        Adds the credit column to the dataframe

        :param dataframe: The dataframe to add the credit column
        :type dataframe: pd.DataFrame
        :param type_application: The type of application to calculate credit
        :type type_application: str
        :return: The dataframe with the credit column
        :rtype: pd.DataFrame
        """
        if type_application == "P_BASE":
            dataframe['P. Crédito'] = trunc_number(
                dataframe['PVP'] * (1 + dataframe['Dto. Factura'] - dataframe['Bonificación']), 3
            )
        else:
            dataframe['P. Crédito'] = trunc_number(
                dataframe['PVP'] * (1 + dataframe['Dto. Factura']), 3
            )
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
            dataframe['APORTE'] = trunc_number(
                dataframe['PVP'] * dataframe['Bonificación'], 3) * dataframe['CTD_SACOS'] * (1 + dataframe['Dto. Adicional']
            )
        else:
            dataframe['APORTE'] = dataframe['P. Crédito'] * (1 + dataframe['Dto. Adicional']) * dataframe['Bonificación'] * dataframe['CTD_SACOS']
        return dataframe
