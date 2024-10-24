"""
A module for cleaning in the engineering-transformation-preprocessing-cleaning package.
"""

import pandas as pd

from config.settings import Settings
from engineering.transformation.preprocessing.cleaning.process.process import (
    process_client,
    process_sellout,
    process_binnacle,
    process_price,
    process_sale,
)


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
    processed_sales: pd.DataFrame = process_sale(data["sales"], settings.sales)

    return {
        "clients": processed_clients,
        "sellout": processed_sellout,
        "binnacle": processed_binnacle,
        "prices": processed_prices,
        "sales": processed_sales
    }
