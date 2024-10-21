"""
This module integrates the data for the upcoming transformation process
"""

import logging

import pandas as pd

from config.settings import Settings
from core.decorators import with_logging
from engineering.transformation.preprocessing.integration.sales import SaleAssembler
from engineering.transformation.preprocessing.integration.sellout import SellOutAssembler

logger: logging.Logger = logging.getLogger(__name__)


def integrate_sellout(
    sellout_df: pd.DataFrame, binnacle_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Integrate pricing data along with SKU metadata

    :param sellout_df: The sellout data to integrate
    :type sellout_df: pd.DataFrame
    :param binnacle_df: The binnacle data to integrate
    :type binnacle_df: pd.DataFrame
    :return: The assembled information for pricing
    :rtype: pd.DataFrame
    """
    sellout_assembler: SellOutAssembler = SellOutAssembler()
    assembled_sellout: pd.DataFrame = sellout_assembler.filter_sellout(
        sellout_df, binnacle_df
    )
    return assembled_sellout

def integrate_sales(
    sales_df: pd.DataFrame, clients_df: pd.DataFrame, binnacle_df: pd.DataFrame, settings: Settings
) -> pd.DataFrame:
    """
    Integrate pricing data along with SKU metadata

    :param sales_df: The sales data to integrate
    :type sales_df: pd.DataFrame
    :param clients_df: The clients data to integrate
    :type clients_df: pd.DataFrame
    :param binnacle_df: The binnacle data to integrate
    :type binnacle_df: pd.DataFrame
    :param settings: The settings for the integration
    :type settings: Settings
    :return: The assembled information for pricing
    :rtype: pd.DataFrame
    """
    sales_assembler: SaleAssembler = SaleAssembler(settings)
    merged_sales: pd.DataFrame = sales_assembler.merged_sales(
        sales_df, clients_df
    )
    assembled_sales: pd.DataFrame = sales_assembler.filter_sales(
        merged_sales, binnacle_df
    )
    return assembled_sales

@with_logging
def integrate(
    data: dict[str, pd.DataFrame],
    settings: Settings,
) -> dict[str, pd.DataFrame]:
    """
    Integrate clean data for the upcoming transformation process

    :param data: The data to integrate
    :type data: dict[str, pd.DataFrame]
    :param settings: The settings for the integration
    :type settings: Settings
    :return: The updated data for the transformation
    :rtype: dict[str, pd.DataFrame]
    """
    integrated_sellout: pd.DataFrame = integrate_sellout(
        data["sellout"], data["binnacle"]
    )
    integrated_sales: pd.DataFrame = integrate_sales(
        data["sales"], data["clients"], data["binnacle"], settings
    )
    logger.info("Preprocessing integration finished")
    return {
        "sellout": integrated_sellout,
        "sales": integrated_sales,
    }
