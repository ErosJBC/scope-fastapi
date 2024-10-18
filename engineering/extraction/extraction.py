"""
A module for extraction in the engineering package.
"""

import logging

import pandas as pd

from config.settings import Settings
from core.decorators import with_logging
from core.manager import load_file
from schemas.binnacle import Binnacle
from schemas.client import Client
from schemas.price import Price
from schemas.sale import Sale
from schemas.sellout import SellOut

logger: logging.Logger = logging.getLogger(__name__)


@with_logging
def extract(settings: Settings) -> dict[str, pd.DataFrame]:
    """
    Extraction function for the data pipeline on raw data

    :param settings: The settings to extract the data
    :type settings: Settings
    :return: A dictionary that contains the extracted dataframes
    :rtype: dict[str, pd.DataFrame]
    """
    binnacle: pd.DataFrame = load_file(settings.binnacle, Binnacle)
    clients: pd.DataFrame = load_file(settings.clients, Client)
    prices: pd.DataFrame = load_file(settings.prices, Price)
    sales: pd.DataFrame = load_file(settings.sales, Sale)
    sellout: pd.DataFrame = load_file(settings.sellout, SellOut)
    logger.info("Data extracted")
    return {
        "binnacle": binnacle,
        "clients": clients,
        "prices": prices,
        "sales": sales,
        "sellout": sellout,
    }
