"""
A module for cleaning in the engineering-transformation-preprocessing-cleaning
 package.
"""

import logging

import pandas as pd

from config.settings import Settings
from core.decorators import with_logging
from engineering.transformation.preprocessing.cleaning.process.process import (
    process_client,
    process_sellout,
    process_binnacle,
    process_price,
    process_sale,
)

logger: logging.Logger = logging.getLogger(__name__)


@with_logging
def clean(
    data: dict[str, pd.DataFrame], settings: Settings
) -> dict[str, pd.DataFrame]:
    """
    Clean the raw data from the given dictionary

    :param data: The raw data to be processed
    :type data: dict[str, pd.DataFrame]
    :param settings: The settings to be used
    :type settings: Settings
    :return: The processed data
    :rtype: dict[str, pd.DataFrame]
    """
    processed_binnacle: pd.DataFrame = process_binnacle(data["binnacle"], settings.binnacle)
    processed_clients: pd.DataFrame = process_client(data["clients"], settings.clients)
    processed_prices: pd.DataFrame = process_price(data["prices"], settings.prices)

    processed_sellout: pd.DataFrame = process_sellout(data["sellout"], settings.sellout)
    filtered_sellout = processed_sellout[processed_sellout['COD_ZNJE'].isin(processed_binnacle['COD_ZNJE'].unique())].copy()
    filtered_sellout.reset_index(drop=True, inplace=True)

    processed_sales: pd.DataFrame = process_sale(data["sales"], settings.sales)
    merged_sales = processed_sales.merge(processed_clients[settings.clients.FILTER_COLUMNS], on=settings.sales.MERGE_COLUMNS, how='left')
    filtered_sales = merged_sales[merged_sales['COD_ZNJE'].isin(processed_binnacle['COD_ZNJE'].unique())].copy()
    filtered_sales.sort_values(by=['YEAR', 'MONTH'], inplace=True)
    filtered_sales.reset_index(drop=True, inplace=True)

    logger.info("Cleaning finished")
    return {
        "clients": processed_clients,
        "sellout": filtered_sellout,
        "binnacle": processed_binnacle,
        "prices": processed_prices,
        "sales": filtered_sales
    }
