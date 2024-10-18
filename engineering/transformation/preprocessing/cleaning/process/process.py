"""
A module for filter in the engineering-transformation-preprocessing-cleaning
-filter package.
"""

import pandas as pd

from config.settings import (
    ClientSettings,
    BinnacleSettings,
    SellOutSettings,
    PriceSettings,
    SaleSettings
)
from engineering.transformation.preprocessing.cleaning.process.client import ClientProcess
from engineering.transformation.preprocessing.cleaning.process.binnacle import BinnacleProcess
from engineering.transformation.preprocessing.cleaning.process.sellout import SellOutProcess
from engineering.transformation.preprocessing.cleaning.process.price import PriceProcess
from engineering.transformation.preprocessing.cleaning.process.sale import SaleProcess


def process_client(
    dataframe: pd.DataFrame, client_settings: ClientSettings
) -> pd.DataFrame:
    """
    Process clients data using the given settings

    :param dataframe: The raw dataframe to filter
    :type dataframe: pd.DataFrame
    :param client_settings: The client settings instance
    :type client_settings: ClientSettings
    :return: The process clients dataframe
    :rtype: pd.DataFrame
    """
    client_process: ClientProcess = ClientProcess(client_settings)
    filtered_client: pd.DataFrame = client_process.filter_countries(dataframe)
    unique_client = filtered_client.drop_duplicates().reset_index(drop=True)
    return unique_client

def process_binnacle(
    dataframe: pd.DataFrame, binnacle_settings: BinnacleSettings
) -> pd.DataFrame:
    """
    Process binnacle data using the given settings

    :param dataframe: The raw dataframe to filter
    :type dataframe: pd.DataFrame
    :param binnacle_settings: The binnacle settings instance
    :type binnacle_settings: BinnacleSettings
    :return: The process binnacle dataframe
    :rtype: pd.DataFrame
    """
    binnacle_process: BinnacleProcess = BinnacleProcess(binnacle_settings)
    status_binnacle: pd.DataFrame = binnacle_process.filter_status(dataframe)
    via_binnacle: pd.DataFrame = binnacle_process.filter_via(status_binnacle)
    renamed_binnacle: pd.DataFrame = binnacle_process.rename_columns_dataframe(via_binnacle)
    return renamed_binnacle

def process_sellout(
    dataframe: pd.DataFrame, sellout_settings: SellOutSettings
) -> pd.DataFrame:
    """
    Process sellout data using the given settings

    :param dataframe: The raw dataframe to filter
    :type dataframe: pd.DataFrame
    :param sellout_settings: The sellout settings instance
    :type sellout_settings: SellOutSettings
    :return: The process sellout dataframe
    :rtype: pd.DataFrame
    """
    sellout_process: SellOutProcess = SellOutProcess(sellout_settings)
    type_sellout: pd.DataFrame = sellout_process.filter_type(dataframe)
    added_columns_sellout: pd.DataFrame = sellout_process.add_columns(type_sellout)
    renamed_sellout: pd.DataFrame = sellout_process.rename_columns_dataframe(added_columns_sellout)
    renamed_sellout['ETAPA'] = renamed_sellout['ETAPA'].str.capitalize()
    renamed_sellout.sort_values(by=['YEAR', 'MONTH'], inplace=True)
    return renamed_sellout

def process_price(
    dataframe: pd.DataFrame, price_settings: PriceSettings
) -> pd.DataFrame:
    """
    Process price data using the given settings

    :param dataframe: The raw dataframe to filter
    :type dataframe: pd.DataFrame
    :param price_settings: The price settings instance
    :type price_settings: PriceSettings
    :return: The process price dataframe
    :rtype: pd.DataFrame
    """
    price_process: PriceProcess = PriceProcess(price_settings)
    consider_price: pd.DataFrame = price_process.filter_consider(dataframe)
    status_sku_price: pd.DataFrame = price_process.filter_status_sku(consider_price)
    renamed_price: pd.DataFrame = price_process.rename_columns_dataframe(status_sku_price).reset_index(drop=True)
    renamed_price.drop_duplicates(subset=['COD_ZNJE', 'COD_PRODUCTO'], keep='last', inplace=True)
    renamed_price['COD_ZNJE'] = renamed_price['COD_ZNJE'].astype(int)
    renamed_price['COD_PRODUCTO'] = renamed_price['COD_PRODUCTO'].astype(int)
    renamed_price['Dto. Factura'] = renamed_price['Dto. Factura'] / 100
    return renamed_price

def process_sale(
    dataframe: pd.DataFrame, sale_settings: SaleSettings
) -> pd.DataFrame:
    """
    Process sale data using the given settings

    :param dataframe: The raw dataframe to filter
    :type dataframe: pd.DataFrame
    :param sale_settings: The sale settings instance
    :type sale_settings: SaleSettings
    :return: The process sale dataframe
    :rtype: pd.DataFrame
    """
    sale_process: SaleProcess = SaleProcess(sale_settings)
    added_columns_sale: pd.DataFrame = sale_process.add_columns(dataframe)
    renamed_sale: pd.DataFrame = sale_process.rename_columns_dataframe(added_columns_sale)
    return renamed_sale
