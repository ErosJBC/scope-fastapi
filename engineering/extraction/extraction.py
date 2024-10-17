"""
A module for extraction in the engineering package.
"""

import logging

import pandas as pd

from config.settings import Settings
from core.decorators import with_logging
from core.persistence_manager import load_file
from schemas.base_prices import BasePrice
from schemas.cash_total_sales import CashTotalSales
from schemas.client import Client
from schemas.demand import Demand
from schemas.price import Price
from schemas.sales import Sales
from schemas.sku import SKU

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
    clients: pd.DataFrame = load_file(settings.clients, Client)
    sku: pd.DataFrame = load_file(settings.skus, SKU)
    demand: pd.DataFrame = load_file(settings.demand, Demand)
    cash_sales: pd.DataFrame = load_file(settings.cash, CashTotalSales)
    sales: pd.DataFrame = load_file(settings.sales, Sales)
    prices: pd.DataFrame = load_file(settings.prices, Price)
    base_prices: pd.DataFrame = load_file(settings.base_prices, BasePrice)
    logger.info("Data extracted")
    return {
        "clients": clients,
        "sku": sku,
        "demand": demand,
        "cash_sales": cash_sales,
        "sales": sales,
        "prices": prices,
        "base_prices": base_prices,
    }
